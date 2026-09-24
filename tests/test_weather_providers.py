# tests/test_weather_providers.py
import pytest
import requests
from datetime import datetime

from modules.weather_providers import (
    get_provider,
    OpenWeatherMapOneCallProvider,
    MeteoblueProvider,
    ITWHProvider,
    OpenMeteoProvider,
    _to_gmt1,
)


# ---------- Fixtures: Beispiel-Responses der APIs ----------

@pytest.fixture
def owm_onecall_response():
    return {
        "current": {"dt": 1717000000, "rain": {"1h": 0.5}},
        "hourly": [
            {"dt": 1717000000, "rain": {"1h": 0.5}},
            {"dt": 1717003600, "rain": {"1h": 0.0}},
            {"dt": 1717007200},  # kein "rain"-Key -> Randfall
        ],
    }


@pytest.fixture
def meteoblue_response():
    return {
        "data_1h": {
            "time": ["2024-06-01 12:00", "2024-06-01 13:00"],
            "precipitation": [0.2, 0.0],
        }
    }


@pytest.fixture
def itwh_response():
    return {
        "vorhersageZeit": "2024-06-01 12:00",
        "aktuell": {"2024-06-01 12:00": 50},   # -> 0.5 mm
        "vorhersage": {
            "2024-06-01 12:05": 100,           # -> 1.0 mm
            "2024-06-01 12:10": 0,
        },
    }


@pytest.fixture
def open_meteo_response():
    return {
        "latitude": 53.14,
        "longitude": 8.17,
        "hourly": {
            "time": ["2024-06-01T00:00", "2024-06-01T01:00", "2024-06-01T02:00"],
            "precipitation": [0.0, 0.5, 1.2],
        },
    }


# ---------- OpenWeatherMapProvider ----------

class TestOpenWeatherMapOneCallProvider:
    def test_fetch_normalizes_data(self, requests_mock, owm_onecall_response):
        requests_mock.get(OpenWeatherMapOneCallProvider.BASE_URL,
                          json=owm_onecall_response)

        result = OpenWeatherMapOneCallProvider(
            api_key="dummy").fetch(lat=53.15, lon=8.16)

        assert result["latitude"] == 53.15
        assert result["projected_ppt"] == 0.5
        assert len(result["forecast"]) == 3
        # fehlender "rain"-Key -> 0.0
        assert 0.0 in result["forecast"].values()

    def test_fetch_sends_api_key_and_excludes(self, requests_mock, owm_onecall_response):
        requests_mock.get(OpenWeatherMapOneCallProvider.BASE_URL,
                          json=owm_onecall_response)

        OpenWeatherMapOneCallProvider(api_key="my-secret").fetch(lat=1, lon=1)

        qs = requests_mock.last_request.qs
        assert qs["appid"] == ["my-secret"]
        assert qs["exclude"] == ["minutely,daily,alerts"]

    def test_fetch_raises_on_http_error(self, requests_mock):
        requests_mock.get(
            OpenWeatherMapOneCallProvider.BASE_URL, status_code=401)

        with pytest.raises(requests.exceptions.HTTPError):
            OpenWeatherMapOneCallProvider(
                api_key="invalid").fetch(lat=1, lon=1)

    def test_fetch_error_does_not_leak_key(self, requests_mock):
        requests_mock.get(
            OpenWeatherMapOneCallProvider.BASE_URL, status_code=401)

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            OpenWeatherMapOneCallProvider(
                api_key="geheim123").fetch(lat=1, lon=1)

        assert "geheim123" not in str(exc_info.value)


# ---------- MeteoblueProvider ----------

class TestMeteoblueProvider:
    def test_fetch_normalizes_data(self, requests_mock, meteoblue_response):
        requests_mock.get(MeteoblueProvider.BASE_URL, json=meteoblue_response)

        result = MeteoblueProvider(api_key="dummy").fetch(lat=53.15, lon=8.16)

        assert result["projected_ppt"] == 0.2
        assert result["forecast"] == {
            "2024-06-01 12:00": 0.2,
            "2024-06-01 13:00": 0.0,
        }


# ---------- ITWHProvider ----------

class TestITWHProvider:
    def test_fetch_converts_100mm_to_mm(self, requests_mock, itwh_response):
        requests_mock.get(
            "https://swat.itwh.de/Vorhersage", json=itwh_response
        )
        result = ITWHProvider().fetch(lat=53.15, lon=8.16)

        assert result["projected_ppt"] == 0.5
        assert set(result["forecast"].values()) == {1.0, 0.0}

    def test_fetch_uses_test_url_for_zero_coordinates(self, requests_mock, itwh_response):
        requests_mock.get(
            "https://swat.itwh.de/Vorhersage/GetVorhersageTest", json=itwh_response
        )
        ITWHProvider().fetch(lat=0, lon=0)

        assert "lat=0" in requests_mock.last_request.url


# ---------- OpenMeteoProvider ----------
class TestOpenMeteoProvider:
    def test_fetch_normalizes_data(self, requests_mock, open_meteo_response):
        requests_mock.get(OpenMeteoProvider.BASE_URL, json=open_meteo_response)

        result = OpenMeteoProvider().fetch(lat=53.15, lon=8.16)

        assert result["latitude"] == 53.15
        assert result["longitude"] == 8.16
        assert result["forecast"] == {
            "2024-06-01 00:00": 0.0,
            "2024-06-01 01:00": 0.5,
            "2024-06-01 02:00": 1.2,
        }
        # "date" muss ein tatsächlicher Key aus dem Forecast sein,
        # und projected_ppt muss dazu konsistent sein
        assert result["date"] in result["forecast"]
        assert result["projected_ppt"] == result["forecast"][result["date"]]

    def test_fetch_sends_correct_params_and_no_key(self, requests_mock, open_meteo_response):
        requests_mock.get(OpenMeteoProvider.BASE_URL, json=open_meteo_response)

        OpenMeteoProvider().fetch(lat=1, lon=2)  # kein api_key nötig

        qs = requests_mock.last_request.qs
        assert qs["latitude"] == ["1"]
        assert qs["longitude"] == ["2"]
        assert qs["hourly"] == ["precipitation"]
        assert "appid" not in qs
        assert "apikey" not in qs

    def test_fetch_raises_on_http_error(self, requests_mock):
        requests_mock.get(OpenMeteoProvider.BASE_URL, status_code=400)

        with pytest.raises(requests.exceptions.HTTPError):
            OpenMeteoProvider().fetch(lat=1, lon=1)

    def test_fetch_error_url_is_redacted_consistently(self, requests_mock):
        # Open-Meteo braucht zwar keinen Key, aber die Fehlerbehandlung soll
        # trotzdem denselben (redigierten) Format-String wie die anderen Provider nutzen
        requests_mock.get(OpenMeteoProvider.BASE_URL, status_code=400)

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            OpenMeteoProvider().fetch(lat=1, lon=1)

        assert "400 Error for url" in str(exc_info.value)


# ---------- get_provider() Factory ----------

@pytest.mark.parametrize("name, expected_cls", [
    ("openweathermap-onecall", OpenWeatherMapOneCallProvider),
    ("meteoblue", MeteoblueProvider),
    ("open-meteo", OpenMeteoProvider),
    ("itwh", ITWHProvider),
])
def test_get_provider_returns_correct_class(name, expected_cls):
    assert isinstance(get_provider(name, api_key="key"), expected_cls)


def test_get_provider_raises_on_unknown_name():
    with pytest.raises(ValueError, match="Unbekannter Wetter-Provider"):
        get_provider("unbekannt", api_key="key")


# ---------- _to_gmt1() Helper ----------

def test_to_gmt1_adds_one_hour_in_winter():
    utc_dt = datetime(2024, 1, 1, 12, 0, 0)  # Winterzeit, kein DST
    assert _to_gmt1(utc_dt).hour == 13
