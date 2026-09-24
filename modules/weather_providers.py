from warnings import deprecated

import requests
from datetime import datetime, timezone
import pytz
import copy
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, TypedDict


class WeatherResult(TypedDict):
    """Normalisierte Rückgabe, die jeder Provider liefern muss."""
    date: str                    # "%Y-%m-%d %H:%M", GMT+1
    latitude: float
    longitude: float
    projected_ppt: float         # aktueller Niederschlag in mm
    forecast: Dict[str, float]   # {"%Y-%m-%d %H:%M": mm, ...}


def _to_gmt1(dt_utc: datetime) -> datetime:
    """Konvertiert ein UTC-datetime nach GMT+1 (Europe/Paris als Referenzzone).

    Akzeptiert sowohl naive als auch bereits timezone-aware UTC-Datetimes:
    pytz.localize() wirft einen Fehler, wenn man es auf ein bereits
    "aware" Objekt anwendet, daher die Fallunterscheidung.
    """
    gmt1 = pytz.timezone("Europe/Paris")
    if dt_utc.tzinfo is None:
        dt_utc = pytz.utc.localize(dt_utc)
    return dt_utc.astimezone(gmt1)


def _redact_secrets(url: str) -> str:
    """Entfernt API-Key-Query-Parameter aus einer URL, bevor sie geloggt
    oder in eine Exception-Message eingebettet wird (appid=..., apikey=...).
    Verhindert, dass Keys über Tracebacks/CI-Logs im Klartext landen.
    """
    return re.sub(r"(?i)(appid|apikey)=[^&]+", r"\1=***", url)


class WeatherProvider(ABC):
    """Basis-Interface, das jeder Wetter-Provider implementieren muss."""

    name: str = "base"

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key

    @abstractmethod
    def fetch(self, lat: float, lon: float) -> WeatherResult:
        """Ruft die Wetterdaten für die gegebenen Koordinaten ab und
        normalisiert sie auf das WeatherResult-Format."""
        raise NotImplementedError

    def _request_json(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Gemeinsamer HTTP-GET-Helper für alle Provider.

        Request ausführen, bei Fehlerstatus eine HTTPError werfen, dabei aber
        den API-Key aus der URL redigieren, bevor er in die Exception-Message
        wandert (siehe _redact_secrets).
        """
        response = requests.get(url, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            safe_url = _redact_secrets(response.url)
            # Response-Body mit ausgeben, hilft bei der Fehlersuche (z.B. Meteoblues
            # "datafeed is not authorized for your api key"). Enthält i.d.R. keine
            # Secrets, da der Key nur in der Request-URL steht, nicht im Body.
            body_excerpt = response.text[:300]
            raise requests.exceptions.HTTPError(
                f"{response.status_code} Error for url: {safe_url} - Body: {body_excerpt}",
                response=response,
            ) from None
        return response.json()


class OpenWeatherMapOneCallProvider(WeatherProvider):
    """Nutzt die OpenWeatherMap One Call API 3.0 (separates Abo nötig,
    aber mit 1.000 Free-Calls/Tag). 
    """

    name = "openweathermap-onecall"
    BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

    def fetch(self, lat: float, lon: float) -> WeatherResult:
        params: Dict[str, Any] = {
            "lat": lat, "lon": lon, "appid": self.api_key,
            "units": "metric",
            # minutely/daily/alerts brauchen wir nicht -> spart Payload
            "exclude": "minutely,daily,alerts",
        }
        data = self._request_json(self.BASE_URL, params)

        current_gmt1 = _to_gmt1(
            datetime.fromtimestamp(data["current"]["dt"], tz=timezone.utc))
        current_ppt: float = data["current"].get("rain", {}).get("1h", 0.0)

        forecast: Dict[str, float] = {}
        for hour in data.get("hourly", []):
            ts = _to_gmt1(datetime.fromtimestamp(hour["dt"], tz=timezone.utc))
            # "rain" fehlt komplett im JSON, wenn es zu der Stunde nicht regnet
            forecast[ts.strftime("%Y-%m-%d %H:%M")
                     ] = hour.get("rain", {}).get("1h", 0.0)

        return {
            "date": current_gmt1.strftime("%Y-%m-%d %H:%M"),
            "latitude": lat, "longitude": lon,
            "projected_ppt": current_ppt, "forecast": forecast,
        }


class MeteoblueProvider(WeatherProvider):
    name = "meteoblue"
    BASE_URL = "https://my.meteoblue.com/packages/basic-1h"

    def fetch(self, lat: float, lon: float) -> WeatherResult:
        params: Dict[str, Any] = {
            "lat": lat, "lon": lon, "apikey": self.api_key, "format": "json",
        }
        data = self._request_json(self.BASE_URL, params)

        times = data["data_1h"]["time"]
        precipitation = data["data_1h"]["precipitation"]  # bereits in mm
        forecast: Dict[str, float] = dict(zip(times, precipitation))

        return {
            "date": times[0],
            "latitude": lat, "longitude": lon,
            "projected_ppt": precipitation[0], "forecast": forecast,
        }


class OpenMeteoProvider(WeatherProvider):
    """Braucht keinen API-Key. Liefert nur stündliche Forecast-Werte,
    keinen separaten "current"-Wert -> wir nehmen als projected_ppt den
    Forecast-Eintrag, dessen Zeitstempel am nächsten an "jetzt" liegt.
    """

    name = "open-meteo"
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def fetch(self, lat: float, lon: float) -> WeatherResult:
        params: Dict[str, Any] = {
            "latitude": lat, "longitude": lon,
            "hourly": "precipitation",
            "timezone": "Europe/Berlin",
        }
        data = self._request_json(self.BASE_URL, params)

        times = data["hourly"]["time"]            # z.B. "2024-06-01T12:00"
        precipitation = data["hourly"]["precipitation"]
        forecast: Dict[str, float] = {
            t.replace("T", " "): p for t, p in zip(times, precipitation)
        }

        # Nächstliegenden Stundenwert als "aktuellen" Wert verwenden, da
        # Open-Meteo hier keinen expliziten current-Wert liefert.
        now_key = min(
            forecast,
            key=lambda t: abs(datetime.strptime(
                t, "%Y-%m-%d %H:%M") - datetime.now())
        )

        return {
            "date": now_key,
            "latitude": lat, "longitude": lon,
            "projected_ppt": forecast[now_key], "forecast": forecast,
        }


@deprecated("The ITWH-Provider is not working reliably. Use any other provider instead.")
class ITWHProvider(WeatherProvider):
    """
    Legacy-Provider. 
    """

    name = "itwh"
    BASE_URL = "https://swat.itwh.de/Vorhersage"

    @deprecated("The ITWH-Provider is not working reliably. Use any other provider instead.")
    def fetch(self, lat: float, lon: float) -> WeatherResult:
        params: Dict[str, Any] = {"lat": lat, "lon": lon}

        url = self.BASE_URL
        if lat == 0 and lon == 0:
            url = "https://swat.itwh.de/Vorhersage/GetVorhersageTest"
            print("Using test data")

        data = self._request_json(url, params)
        converted_data = self._convert_json_to_gmt1(data)

        return {
            "date": converted_data["vorhersageZeit"],
            "latitude": float(lat),
            "longitude": float(lon),
            "projected_ppt": converted_data["aktuell"][converted_data["vorhersageZeit"]] / 100,
            "forecast": self._convert_100mm_to_mm(converted_data["vorhersage"]),
        }

    def _convert_100mm_to_mm(self, values: Dict[str, float]) -> Dict[str, float]:
        for key in values:
            values[key] = values[key] / 100
        return values

    def _convert_timestamp_to_gmt1(self, timestamp: str) -> str:
        """Konvertiert einen einzelnen ITWH-Zeitstempel (naiv, UTC) nach GMT+1."""
        utc_datetime = pytz.timezone("UTC").localize(
            datetime.strptime(timestamp, "%Y-%m-%d %H:%M"))
        return utc_datetime.astimezone(pytz.timezone("Europe/Paris")).strftime("%Y-%m-%d %H:%M")

    def _convert_json_to_gmt1(self, input_json: Dict[str, Any]) -> Dict[str, Any]:
        converted_json = copy.deepcopy(input_json)

        converted_json["vorhersageZeit"] = self._convert_timestamp_to_gmt1(
            input_json["vorhersageZeit"])

        # "aktuell" hat genau einen Eintrag (Zeitstempel -> Wert);
        # dessen Key muss ebenfalls auf GMT+1 umgerechnet werden.
        keys = list(input_json["aktuell"].keys())
        converted_key = self._convert_timestamp_to_gmt1(keys[0])
        converted_json["aktuell"][converted_key] = input_json["aktuell"].pop(
            keys[0])

        converted_json["vorhersage"] = {
            self._convert_timestamp_to_gmt1(ts): value
            for ts, value in input_json["vorhersage"].items()
        }

        return converted_json


PROVIDERS: Dict[str, Type[WeatherProvider]] = {
    OpenWeatherMapOneCallProvider.name: OpenWeatherMapOneCallProvider,
    MeteoblueProvider.name: MeteoblueProvider,
    OpenMeteoProvider.name: OpenMeteoProvider,
    ITWHProvider.name: ITWHProvider,
}


def get_provider(name: str, api_key: Optional[str] = None) -> WeatherProvider:
    try:
        return PROVIDERS[name](api_key=api_key)
    except KeyError:
        raise ValueError(
            f"Unbekannter Wetter-Provider '{name}'. Verfügbar: {', '.join(PROVIDERS)}")
