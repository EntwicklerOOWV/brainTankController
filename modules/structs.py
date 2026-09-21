import requests
from datetime import datetime
import pytz

from modules.configuration import user_config
from modules.weather_providers import get_provider


class WeatherData:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        cls._instance = super().__new__(cls)
        initResult = cls._instance._initialize_data()
        if (initResult == False):
            return None
        else:
            return cls._instance

    def _initialize_data(self):
        lat = user_config.latitude
        lon = user_config.longitude
        if lat is None and lon is None:
            return False

        try:
            provider = get_provider(
                user_config.weather_provider, user_config.weather_api_key)
            result = provider.fetch(lat, lon)
            self._date = result["date"]
            self._latitude = result["latitude"]
            self._longitude = result["longitude"]
            self._projected_ppt = result["projected_ppt"]
            self._forecast = result["forecast"]
            return True
        except (requests.exceptions.RequestException, ValueError) as e:
            print("Error while fetching weather data:", e)
            return False

    @property
    def date(self):
        return self._date

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def projected_ppt(self):
        return self._projected_ppt

    @property
    def forecast(self):
        return self._forecast


class Task:
    __instance = None

    def __new__(cls, task="default"):
        if not cls.__instance:
            cls.__instance = super(Task, cls).__new__(cls)
            cls.__instance.task = task
            cls.__instance.drain_value = None
            cls.__instance.drain_stopped = False
        return cls.__instance

    def current_task(self):
        return self.task

    def set_task(self, task, value):
        self.task = task
        if task == "threshold_drain":
            self.drain_value = value
        else:
            self.drain_value = None

    def get_task_value(self):
        if self.task == "threshold_drain":
            return self.drain_value
        else:
            return 0

    def set_drain_stopped(self, mode):
        self.drain_stopped = mode


task = Task()
