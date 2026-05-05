import sys

import secret_configs
from logger import Logger


ENVIRONMENT = secret_configs.ENVIRONMENT

WIFI_SSID = secret_configs.WIFI_SSID
WIFI_PWD = secret_configs.WIFI_PWD

# MQTT SETTINGS
MQTT_TOPIC = secret_configs.MQTT_TOPIC
AWS_IOT_ENDPOINT = secret_configs.AWS_IOT_ENDPOINT
MQTT_PORT = 8883
MQTT_CLIENT_ID = secret_configs.MQTT_CLIENT_ID
MQTT_KEEPALIVE = 60
MQTT_CHECK_MESSAGE_INTERVAL = 0.5
MQTT_PING_INTERVAL = 35

# CREDENTIALS SETUP
AWS_CERT_FILE = secret_configs.AWS_CERT_FILE
AWS_PRIVATE_KEY_FILE = secret_configs.AWS_PRIVATE_KEY_FILE

# LOGGING SETUP
logger = Logger()
