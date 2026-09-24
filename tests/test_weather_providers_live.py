from modules.weather_providers import (
    OpenWeatherMapOneCallProvider,
    MeteoblueProvider,
    OpenMeteoProvider,
    ITWHProvider,
)
import os
from datetime import datetime
import pytest


pytestmark = pytest.mark.integration


def _require_key(env_var):
    key = os.environ.get(env_var)
    if not key:
        pytest.skip(f"{env_var} nicht gesetzt – Live-Test übersprungen")
    return key


def _assert_forecast_schema(result):
    assert isinstance(result["date"], str)
    assert isinstance(result["latitude"], float)
    assert isinstance(result["longitude"], float)
    assert isinstance(result["projected_ppt"], (int, float))
    assert isinstance(result["forecast"], dict)
    assert len(result["forecast"]) > 0

    # Stichprobe: Zeitformat + Werttyp eines Forecast-Eintrags prüfen
    ts, value = next(iter(result["forecast"].items()))
    # wirft ValueError bei falschem Format
    datetime.strptime(ts, "%Y-%m-%d %H:%M")
    assert isinstance(value, (int, float))


class TestOpenWeatherMapOneCallLive:
    def test_response_matches_expected_schema(self):
        # eigener Env-Var-Name, weil dieser Key zwingend das One-Call-3.0-
        # Abo braucht -- ein normaler OWM_TEST_API_KEY reicht hier NICHT
        key = _require_key("OWM_ONECALL_TEST_API_KEY")
        result = OpenWeatherMapOneCallProvider(
            api_key=key).fetch(lat=53.1557, lon=8.1654)
        _assert_forecast_schema(result)


class TestMeteoblueLive:
    def test_response_matches_expected_schema(self):
        key = _require_key("METEOBLUE_TEST_API_KEY")
        result = MeteoblueProvider(api_key=key).fetch(lat=53.1557, lon=8.1654)
        _assert_forecast_schema(result)


class TestOpenMeteoLive:
    def test_response_matches_expected_schema(self):
        # kein API-Key nötig -> kein _require_key()
        result = OpenMeteoProvider().fetch(lat=53.1557, lon=8.1654)
        _assert_forecast_schema(result)


@pytest.mark.xfail(reason="ITWH-Testendpoint aktuell mit abgelaufenem TLS-Zertifikat")
class TestItwhLive:
    def test_response_matches_expected_schema(self):

        result = ITWHProvider().fetch(lat=0.0, lon=0.0)
        _assert_forecast_schema(result)
