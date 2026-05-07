import ssl

import ujson
import utime

from settings import logger
from umqtt.simple import MQTTClient
from utils import files


class Mqtt:
    def __init__(
        self,
        device_cert_file_path: str,
        private_key_file_path: str,
        root_ca_file_path: str,
        client_id: str,
        keepalive: int,
        mqtt_endpoint: str,
        mqtt_port: int,
        topics: list[str],
        callback,
    ) -> None:
        self._root_ca_file_path = root_ca_file_path
        self._device_cert_file_path = device_cert_file_path
        self._private_key_file_path = private_key_file_path
        self._callback = callback
        self._client_id = client_id
        self._keepalive = keepalive
        self._mqtt_endpoint = mqtt_endpoint
        self._mqtt_port = mqtt_port
        self._topics = topics

        self._client: MQTTClient = None

        # check if necessary files exist
        if self._root_ca_file_path and not files.check_file_exists(self._root_ca_file_path):
            raise FileNotFoundError(
                f'{self._root_ca_file_path} file is missing!')
        elif not self._root_ca_file_path:
            logger.warning('Skipping MQTT server cert verification')
        if not files.check_file_exists(self._private_key_file_path):
            raise FileNotFoundError(
                f'{self._private_key_file_path} file is missing!')
        if not files.check_file_exists(self._device_cert_file_path):
            raise FileNotFoundError(
                f'{self._device_cert_file_path} file is missing!')

        # put together ssl params
        with open(self._root_ca_file_path, 'rb') as f:
            CA_CERT = f.read()
        with open(self._device_cert_file_path, 'rb') as f:
            DEVICE_CERT = f.read()
        with open(self._private_key_file_path, 'rb') as f:
            PRIVATE_KEY = f.read()
        ssl_params = {
            "cert": DEVICE_CERT,
            "key": PRIVATE_KEY,
            "server_side": False,
            "cert_reqs": ssl.CERT_REQUIRED,
            "server_hostname":self._mqtt_endpoint,
            "cadata": CA_CERT,
        }

        client = None
        try:
            client = MQTTClient(
                client_id=self._client_id,
                server=self._mqtt_endpoint,
                port=self._mqtt_port,
                keepalive=self._keepalive,
                ssl=True,
                ssl_params=ssl_params,
            )
            logger.info("Connecting to AWS IoT...")
            client.connect()

        except Exception as e:
            if client:
                try:
                    client.disconnect()
                except:
                    pass
            logger.error(f"Unable to connect to MQTT: {e}")
            return None

        self._client = client
        logger.info("Connected to MQTT")

        self._client.set_callback(self._callback)
        logger.info('Callback has been set')

        for topic in self._topics:
            self._client.subscribe(topic)
            logger.info(f'Subscribed to {topic}')
            utime.sleep(0.1)

    def is_connected(self):
        return bool(self._client)

    def disconnect(self):
        try:
            self._client.disconnect()
        except:
            pass

    def wait_for_message(self):
        if not self.is_connected():
            logger.error(
                "MQTT client is not connected, cannot wait for messages")
            return
        self._client.wait_msg()

    def check_message(self):
        if not self.is_connected():
            logger.error("MQTT client is not connected, cannot check messages")
            return
        self._client.check_msg()

    def ping(self):
        if not self.is_connected():
            logger.error("MQTT client is not connected, cannot ping")
            return
        self._client.ping()

    def publish(self, topic: str, payload: str | dict, qos: int = 0):
        if not self.is_connected():
            logger.error("MQTT client is not connected, cannot publish")
            return
        if isinstance(payload, dict):
            payload = ujson.dumps(payload)
        self._client.publish(topic, payload, qos=qos)

    def update_shadow(self, topic: str, payload: dict, qos: int = 1):
        if not self.is_connected():
            logger.error("MQTT client is not connected, cannot publish")
            return
        self._client.publish(topic, ujson.dumps(payload), qos=qos)
