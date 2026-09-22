import requests
from datetime import datetime, timezone
import pytz
import copy


def _to_gmt1(dt_utc):
    utc = pytz.timezone("UTC")
    gmt1 = pytz.timezone("Europe/Paris")
    return utc.localize(dt_utc).astimezone(gmt1)


class WeatherProvider:
    """Basis-Interface, das jeder Provider implementieren muss."""
    name = "base"

    def __init__(self, api_key=None):
        self.api_key = api_key

    def fetch(self, lat: float, lon: float):
        """
        Muss ein normalisiertes Dict zurückgeben:
          date: "%Y-%m-%d %H:%M" (GMT+1)
          latitude, longitude: float
          projected_ppt: aktueller Niederschlag in mm
          forecast: {"%Y-%m-%d %H:%M": mm, ...}
        """
        raise NotImplementedError


class OpenWeatherMapProvider(WeatherProvider):
    name = "openweathermap"
    BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

    def fetch(self, lat, lon):
        params = {
            "lat": lat, "lon": lon, "appid": self.api_key,
            "units": "metric", "exclude": "minutely,daily,alerts",
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        current_gmt1 = _to_gmt1(
            datetime.utcfromtimestamp(data["current"]["dt"]))
        current_ppt = data["current"].get("rain", {}).get("1h", 0.0)

        forecast = {}
        for hour in data.get("hourly", []):
            ts = _to_gmt1(datetime.fromtimestamp(hour["dt"], tz=timezone.utc))
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

    def fetch(self, lat, lon):
        params = {"lat": lat, "lon": lon,
                  "apikey": self.api_key, "format": "json"}
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        times = data["data_1h"]["time"]
        precipitation = data["data_1h"]["precipitation"]
        forecast = dict(zip(times, precipitation))  # bereits in mm

        return {
            "date": times[0],
            "latitude": lat, "longitude": lon,
            "projected_ppt": precipitation[0], "forecast": forecast,
        }


class ITWHProvider(WeatherProvider):
    name = "itwh"
    BASE_URL = "https://swat.itwh.de/Vorhersage/GetVorhersageTest"

    def fetch(self, lat, lon):
        params = {"lat": lat, "lon": lon}

        url = self.BASE_URL
        if lat == 0 and lon == 0:
            url = "https://swat.itwh.de/Vorhersage/GetVorhersageTest?lat=0&lon=0"
            print("Using test data")

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        converted_data = self._convert_json_to_gmt1(data)

        return {
            "date": converted_data["vorhersageZeit"],
            "latitude": lat,
            "longitude": lon,
            "projected_ppt": converted_data["aktuell"][converted_data["vorhersageZeit"]]/100,
            "forecast": self._convert_100mm_to_mm(converted_data["vorhersage"]),
        }

    def _convert_100mm_to_mm(self, dict):
        for key in dict:
            dict[key] = dict[key] / 100
        return dict

    def _convert_timestamp_to_gmt1(self, timestamp):
        """Function to convert a single timestamp to GMT+1

        Args:
            timestamp (_type_): _description_

        Returns:
            _type_: _description_
        """
        utc_timezone = pytz.timezone("UTC")
        # Change to the appropriate timezone identifier
        gmt1_timezone = pytz.timezone("Europe/Paris")

        # Convert string to datetime object
        utc_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")

        # Set UTC timezone
        utc_datetime = utc_timezone.localize(utc_datetime)

        # Convert to GMT+1 timezone
        gmt1_datetime = utc_datetime.astimezone(gmt1_timezone)

        # Format the result as a string
        return gmt1_datetime.strftime("%Y-%m-%d %H:%M")

    def _convert_json_to_gmt1(self, input_json):
        # Apply the conversion to all timestamps in the JSON
        converted_json = copy.deepcopy(input_json)
        converted_json["vorhersageZeit"] = self._convert_timestamp_to_gmt1(
            input_json["vorhersageZeit"])

        keys = list(input_json["aktuell"].keys())
        converted_key = self._convert_timestamp_to_gmt1(keys[0])
        converted_json["aktuell"][converted_key] = input_json["aktuell"].pop(
            keys[0])

        converted_dict = {}

        for timestamp, value in input_json["vorhersage"].items():
            converted_timestamp = self._convert_timestamp_to_gmt1(timestamp)
            converted_dict[converted_timestamp] = value

        converted_json["vorhersage"] = converted_dict

        return converted_json


PROVIDERS = {
    OpenWeatherMapProvider.name: OpenWeatherMapProvider,
    MeteoblueProvider.name: MeteoblueProvider,
    ITWHProvider.name: ITWHProvider,
}


def get_provider(name, api_key):
    try:
        return PROVIDERS[name](api_key=api_key)
    except KeyError:
        raise ValueError(
            f"Unbekannter Wetter-Provider '{name}'. Verfügbar: {', '.join(PROVIDERS)}")
