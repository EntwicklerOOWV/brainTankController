import requests

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
    
        url = "https://swat.itwh.de/Vorhersage?lat={}&lon={}".format(lat, lon)

        try:
            json_data = self._request_json_data(url)
            self._date = json_data["vorhersageZeit"]
            self._latitude = json_data["lat"]
            self._longitude = json_data["lon"]
            self._projected_ppt = json_data["aktuell"][json_data["vorhersageZeit"]]
            self._forecast = json_data["vorhersage"]
            return True
        except requests.exceptions.RequestException as e:
            print("Error while fetching data:", e)
            return False
        
    def _request_json_data(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

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