# Ref
# https://aws.amazon.com/blogs/iot/using-micropython-to-get-started-with-aws-iot-core/
# https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.simple/umqtt/simple.py
# https://github.com/aws-samples/aws-iot-core-getting-started-micropython

import time

import ujson

from utils.mqtt import Mqtt
from settings import (AWS_DEVICE_CERT_FILE, AWS_ROOT_CA_FILE, AWS_IOT_ENDPOINT, AWS_PRIVATE_KEY_FILE,
                      MQTT_CHECK_MESSAGE_INTERVAL, MQTT_CLIENT_ID,
                      MQTT_KEEPALIVE, MQTT_PING_INTERVAL, MQTT_PORT,
                      MQTT_TOPIC, WIFI_PWD, WIFI_SSID, logger)
from utils.wlan import Wlan


def callback_func(topic, msg):
    message = ujson.loads(msg)
    logger.info(f'Message received: {message}')


# Connect to WiFi
while True:
    try:
        logger.info('Attempting to connect to WiFi')
        wlan = Wlan(ssid=WIFI_SSID, pwd=WIFI_PWD)
        wlan.connect()

        # mqtt connect
        while True:
            logger.info('Attempting to connect to MQTT')
            mqtt = Mqtt(
                root_ca_file_path=AWS_ROOT_CA_FILE,
                device_cert_file_path=AWS_DEVICE_CERT_FILE,
                private_key_file_path=AWS_PRIVATE_KEY_FILE,
                client_id=MQTT_CLIENT_ID,
                keepalive=MQTT_KEEPALIVE,
                mqtt_endpoint=AWS_IOT_ENDPOINT,
                mqtt_port=MQTT_PORT,
                topics=[MQTT_TOPIC],
                callback=callback_func
            )

            if not mqtt.is_connected():
                time.sleep(2)
                continue

            # initialize last pinged time
            last_pinged = time.time()

            # wait for message
            while True:
                now = time.time()

                if now - last_pinged >= MQTT_PING_INTERVAL:
                    last_pinged = now
                    mqtt.ping()

                mqtt.check_message()
                time.sleep(MQTT_CHECK_MESSAGE_INTERVAL)

    except Exception as e:
        logger.error(f'Exception occured: {e}')
