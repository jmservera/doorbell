#!/usr/bin/python3
# Uses edge detection to limit the rate of Mqtt-messages
import configparser
import sys
import time
from signal import pause

from . import logger
from .raspberry_pi import rpi
from .transport import transport

_rpi: rpi
ring_running = False
ring_count = 0
messages = transport()


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
                messages.send_message('{ "on": ' + str(ring_count) + " }")
                time.sleep(5)
                messages.send_message("off")
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

    _rpi = rpi(config, ring_callback)

    mqtt_user = config["DEFAULT"]["mqtt_user"]
    mqtt_pass = config["DEFAULT"]["mqtt_pass"]
    mqtt_server = config["DEFAULT"]["mqtt_server"]
    mqtt_port = int(config["DEFAULT"]["mqtt_port"])

    # Mqtt
    messages.connect_transport(mqtt_user, mqtt_pass, mqtt_server, mqtt_port)
    messages.on_message = message_received

    logger.info("Starting service")
    messages.send_message("doorbell mqtt started")

    pause()

    messages.stop_transport()


if __name__ == "__main__":
    main(sys.argv[1:])
