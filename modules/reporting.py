import json
import requests
import paho.mqtt.publish as publish
from warnings import deprecated


class ReportingTarget:
    name = "base"

    def send(self, data: dict):
        raise NotImplementedError


@deprecated
class ItwhHttpReporter(ReportingTarget):
    name = "itwh"
    URL = "https://swat.itwh.de/Vorhersage/PostRegentonneData"

    @deprecated
    def send(self, data: dict):
        response = requests.post(
            self.URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        if response.status_code != 200:
            print("Failed to send data via HTTP:",
                  response.status_code, response.text)


class MqttReporter(ReportingTarget):
    name = "mqtt"

    def __init__(self, broker, port, topic, username=None, password=None, use_tls=False):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.auth = {"username": username,
                     "password": password} if username else None
        self.use_tls = use_tls

    def send(self, data: dict):
        try:
            publish.single(
                self.topic,
                payload=json.dumps(data),
                hostname=self.broker,
                port=self.port,
                auth=self.auth,
                tls={} if self.use_tls else None,
                qos=1,
            )
        except Exception as e:
            print("Failed to send data via MQTT:", e)


REPORTERS = {ItwhHttpReporter.name: ItwhHttpReporter,
             MqttReporter.name: MqttReporter}


def get_reporter(user_config):
    target = user_config.reporting_target
    if target == "mqtt":
        return MqttReporter(
            broker=user_config.mqtt_broker,
            port=user_config.mqtt_port,
            topic=user_config.mqtt_topic,
            username=user_config.mqtt_username,
            password=user_config.mqtt_password,
            use_tls=user_config.mqtt_use_tls,
        )
    return ItwhHttpReporter()
