#!/usr/bin/python3
# Uses edge detection to limit the rate of Mqtt-messages
# TODO: implement homekit https://github.com/ikalchev/HAP-python
import configparser
import sys
import time
from signal import pause
from typing import List

from . import logger
from .homekit_transport import homekit_transport
from .interfaces import rpi_interface, transport_interface
from .mqtt_transport import mqtt_transport
from .pi_loader import load_pi

_rpi: rpi_interface
ring_running = False
ring_count = 0

messagers: List[transport_interface] = []


def send_message(msg: str) -> None:
    for messager in messagers:
        messager.send_message(msg)


def message_received(topic: str, message) -> None:
    logger.info(topic + str(message))
    if message == "open":
        logger.info("Opening door")
        _rpi.open_door()


def ring_callback(channel: int) -> None:
    global ring_running, ring_count

    ring_count = ring_count + 1
    if not ring_running:
        ring_running = True
        try:
            if channel:
                logger.info("Fall detected")
                send_message('{ "on": ' + str(ring_count) + " }")
                time.sleep(5)
                send_message("off")
            else:
                logger.info("loop")
        finally:
            ring_running = False
    else:
        logger.info("overlap")
    logger.info("Ring: " + str(ring_count))


def main(argv):
    global _rpi, mqttc, mqtt_server, mqtt_port

    config = configparser.ConfigParser()
    config.read("config.ini")

    _rpi = load_pi(config, ring_callback)

    logger.warning(config.getboolean("DEFAULT", "use_mqtt"))
    if config.getboolean("DEFAULT", "use_mqtt"):
        mqtt_user = config["MQTT"]["mqtt_user"]
        mqtt_pass = config["MQTT"]["mqtt_pass"]
        mqtt_server = config["MQTT"]["mqtt_server"]
        mqtt_port = int(config["MQTT"]["mqtt_port"])

        # Mqtt
        mqtt = mqtt_transport()

        mqtt.connect_transport(mqtt_user, mqtt_pass, mqtt_server, mqtt_port)
        mqtt.on_message = message_received

        messagers.append(mqtt)

    if config.getboolean("DEFAULT", "use_homekit"):
        # Homekit
        homekit = homekit_transport(config["HOMEKIT"]["name"])
        homekit.connect_transport()

        messagers.append(homekit)

    logger.info("Starting service")

    send_message("doorbell mqtt started")

    pause()

    for messager in messagers:
        messager.stop_transport()


if __name__ == "__main__":
    main(sys.argv[1:])
