import requests
from datetime import datetime
import pytz

from modules.configuration import user_config

class WeatherData:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        cls._instance = super().__new__(cls)
        initResult = cls._instance._initialize_data() 
        if(initResult == False): 
            return None
        else:
            return cls._instance

    def _initialize_data(self):
        lat = user_config.latitude
        lon = user_config.longitude

        if lat is None and lon is None:
            return False

        if lat == 0 and lon == 0:
            url = "https://swat.itwh.de/Vorhersage/GetVorhersageTest?lat=0&lon=0"
            print("Using test data")

        else:
            url = "https://swat.itwh.de/Vorhersage?lat={}&lon={}".format(lat, lon)
            print("Using live data")

        try:
            json_data = self._request_json_data(url)
            converted_data = self.convert_json_to_gmt1(json_data)
            self._date = converted_data["vorhersageZeit"]
            self._latitude = converted_data["lat"]
            self._longitude = converted_data["lon"]
            self._projected_ppt = converted_data["aktuell"][converted_data["vorhersageZeit"]]/100
            self._forecast = self.convert_100mm_to_mm(converted_data["vorhersage"])
            return True

        except requests.exceptions.RequestException as e:
            print("Error while fetching data:", e)
            return False
        
    def _request_json_data(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def convert_100mm_to_mm(self, dict):
        for key in dict:
            dict[key] = dict[key] / 100
        return dict

    # Function to convert a single timestamp to GMT+1
    def convert_timestamp_to_gmt1(self, timestamp):
        utc_timezone = pytz.timezone("UTC")
        gmt1_timezone = pytz.timezone("Europe/Paris")  # Change to the appropriate timezone identifier

        # Convert string to datetime object
        utc_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")

        # Set UTC timezone
        utc_datetime = utc_timezone.localize(utc_datetime)

        # Convert to GMT+1 timezone
        gmt1_datetime = utc_datetime.astimezone(gmt1_timezone)

        # Format the result as a string
        return gmt1_datetime.strftime("%Y-%m-%d %H:%M")

    def convert_json_to_gmt1(self, input_json):
        # Apply the conversion to all timestamps in the JSON
        converted_json = input_json.copy()
        converted_json["vorhersageZeit"] = self.convert_timestamp_to_gmt1(input_json["vorhersageZeit"])

        keys = list(input_json["aktuell"].keys())
        converted_key = self.convert_timestamp_to_gmt1(keys[0])
        converted_json["aktuell"][converted_key] = input_json["aktuell"].pop(keys[0])

        converted_dict = {}

        for timestamp, value in input_json["vorhersage"].items():
            converted_timestamp = self.convert_timestamp_to_gmt1(timestamp)
            converted_dict[converted_timestamp] = value

        converted_json["vorhersage"] = converted_dict

        return converted_json

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
    
    def set_drain_stopped(self,mode):
        self.drain_stopped = mode

task = Task()