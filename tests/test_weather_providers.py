# tests/test_weather_providers.py
import pytest
import requests
from datetime import datetime

from modules.weather_providers import (
    get_provider,
    OpenWeatherMapProvider,
    MeteoblueProvider,
    ITWHProvider,
    _to_gmt1,
)


# ---------- Fixtures: Beispiel-Responses der APIs ----------

@pytest.fixture
def owm_response():
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


# ---------- OpenWeatherMapProvider ----------

class TestOpenWeatherMapProvider:
    def test_fetch_normalizes_data(self, requests_mock, owm_response):
        requests_mock.get(OpenWeatherMapProvider.BASE_URL, json=owm_response)

        result = OpenWeatherMapProvider(
            api_key="dummy").fetch(lat=53.15, lon=8.16)

        assert result["latitude"] == 53.15
        assert result["projected_ppt"] == 0.5
        assert len(result["forecast"]) == 3
        # fehlender "rain"-Key -> 0.0
        assert 0.0 in result["forecast"].values()

    def test_fetch_sends_api_key_as_param(self, requests_mock, owm_response):
        requests_mock.get(OpenWeatherMapProvider.BASE_URL, json=owm_response)
        OpenWeatherMapProvider(api_key="my-secret").fetch(lat=1, lon=1)

        assert requests_mock.last_request.qs["appid"] == ["my-secret"]

    def test_fetch_raises_on_http_error(self, requests_mock):
        requests_mock.get(OpenWeatherMapProvider.BASE_URL, status_code=401)

        with pytest.raises(requests.exceptions.HTTPError):
            OpenWeatherMapProvider(api_key="invalid").fetch(lat=1, lon=1)


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
            "https://swat.itwh.de/Vorhersage/GetVorhersageTest", json=itwh_response
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


# ---------- get_provider() Factory ----------

@pytest.mark.parametrize("name, expected_cls", [
    ("openweathermap", OpenWeatherMapProvider),
    ("meteoblue", MeteoblueProvider),
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
