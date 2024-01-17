import json
import requests
import threading
import os


modules_path = os.path.abspath(__file__)
modules_directory = os.path.dirname(modules_path)
configs_directory = os.path.join(modules_directory, '..', 'configs')

dashboard_config_filepath = os.path.join(configs_directory, 'dashboard_config.json')
user_config_filepath = os.path.join(configs_directory, 'user_config.json')
automation_config_filepath = os.path.join(configs_directory, 'automation_config.json')


class Singleton(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=Singleton):
    def __init__(self, file_path, data):
        self.file_path = file_path
        self.data = data
        self.load_from_file()

    def load_from_file(self):
        if self.file_path:
            with open(self.file_path) as f:
                self.data = json.load(f)

    def save_to_file(self):
        if self.file_path:
            with open(self.file_path, 'w') as f:
                json.dump(self.data, f)

    def update_from_json(self, json_url):
        response = requests.get(json_url)
        if response.status_code == 200:
            new_data = response.json()
            self.data.update(new_data)
        else:
            print("Failed to fetch JSON data")

    def get_json(self):
        return json.dumps(self.data)

class DashboardConfig(Config):
    def __init__(self, file_path, data):
        super().__init__(file_path, data)

    @property
    def control_mode(self):
        return self.data.get("control_mode")

    @control_mode.setter
    def control_mode(self, value):
        self.data["control_mode"] = value
        self.save_to_file()

    @property
    def waterlevel(self):
        return self.data.get("waterlevel")

    @waterlevel.setter
    def waterlevel(self, value):
        self.data["waterlevel"] = value
        self.save_to_file()

    @property
    def drain_advised(self):
        return self.data.get("drain_advised")

    @drain_advised.setter
    def drain_advised(self, value):
        self.data["drain_advised"] = value
        self.save_to_file()

    @property
    def is_draining(self):
        return self.data.get("is_draining")

    @is_draining.setter
    def is_draining(self, value):
        self.data["is_draining"] = value
        self.save_to_file()

    @property
    def drain_threshold(self):
        return self.data.get("drain_threshold")

    @drain_threshold.setter
    def drain_threshold(self, value):
        self.data["drain_threshold"] = value
        self.save_to_file()

    @property
    def forecast(self):
        return self.data.get("forecast")

    @forecast.setter
    def forecast(self, value):
        self.data["forecast"] = value
        self.save_to_file()

    @property
    def current_time(self):
        return self.data.get("current_time")

    @current_time.setter
    def current_time(self, value):
        self.data["current_time"] = value
        self.save_to_file()

class UserConfig(Config):
    def __init__(self, file_path, data):
        super().__init__(file_path, data)

    def calculate_total_surface_area(self):
        surfaces = self.data.get("surfaces", [])  # Get the surfaces list from self.data
        total_size = 0
        for surface in surfaces:
            total_size += surface.get("size", 0)
        return total_size

    @property
    def surfaces(self):
        return self.data.get("surfaces")

    @surfaces.setter
    def surfaces(self, value):
        self.data["surfaces"] = value
        self.save_to_file()

    @property
    def player_ids(self):
        return self.data.get("player_ids")
    
    @player_ids.setter
    def player_ids(self, value):
        self.data["player_ids"].append(value)
        self.save_to_file()

    @property
    def longitude(self):
        return self.data.get("longitude")

    @longitude.setter
    def longitude(self, value):
        self.data["longitude"] = value
        self.save_to_file()

    @property
    def latitude(self):
        return self.data.get("latitude")

    @latitude.setter
    def latitude(self, value):
        self.data["latitude"] = value
        self.save_to_file()

class AutomationConfig(Config):
    def __init__(self, file_path, data):
        super().__init__(file_path, data)

    @property
    def ppt_trigger_value(self):
        return self.data.get("ppt_trigger_value")

    @ppt_trigger_value.setter
    def ppt_trigger_value(self, value):
        self.data["ppt_trigger_value"] = value
        self.save_to_file()
    
    @property
    def ppt_trigger_timerange(self):
        return self.data.get("ppt_trigger_timerange")

    @ppt_trigger_timerange.setter
    def ppt_trigger_timerange(self, value):
        self.data["ppt_trigger_timerange"] = value
        self.save_to_file()

    @property
    def preemptive_drain_time(self):
        return self.data.get("preemptive_drain_time")
    
    @preemptive_drain_time.setter
    def preemptive_drain_time(self, value):
        self.data["preemptive_drain_time"] = value
        self.save_to_file()

    @property
    def auto_drain_amount(self):
        return self.data.get("auto_drain_amount")

    @auto_drain_amount.setter
    def auto_drain_amount(self, value):
        self.data["auto_drain_amount"] = value
        self.save_to_file()

    @property
    def user_notify(self):
        return self.data.get("user_notify")

    @user_notify.setter
    def user_notify(self, value):
        self.data["user_notify"] = value
        self.save_to_file()

    @property
    def drain_request(self):
        return self.data.get("drain_request")

    @drain_request.setter
    def drain_request(self, value):
        self.data["drain_request"] = value
        self.save_to_file()

# Config Instances
dashboard_config = DashboardConfig(dashboard_config_filepath, {})
user_config = UserConfig(user_config_filepath, {})
automation_config = AutomationConfig(automation_config_filepath, {})