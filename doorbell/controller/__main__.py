#!/usr/bin/python3
# Uses edge detection to limit the rate of Mqtt-messages
import sys

import time

from signal import pause

from . import logger
import transport

import configparser

from rpi import init_pi, open_door

ring_running = False
ring_count = 0


def message_received(topic: str, message):
    logger.info(topic + str(message))
    if message == "open":
        logger.info("Opening door")
        open_door()


def ring_callback(channel: int) -> None:
    global ring_running, ring_count

    ring_count = ring_count + 1
    if not ring_running:
        ring_running = True
        try:
            if channel:
                logger.info("Fall detected")
                transport.send_message('{ "on": ' + str(ring_count) + " }")
                time.sleep(5)
                transport.send_message("off")
            else:
                logger.info("loop")
        finally:
            ring_running = False
    else:
        logger.info("overlap")
    logger.info("Ring: " + str(ring_count))


def main(argv):

    global mqttc, mqtt_server, mqtt_port

    config = configparser.ConfigParser()
    config.read("config.ini")

    init_pi(config, ring_callback)

    mqtt_user = config["DEFAULT"]["mqtt_user"]
    mqtt_pass = config["DEFAULT"]["mqtt_pass"]
    mqtt_server = config["DEFAULT"]["mqtt_server"]
    mqtt_port = int(config["DEFAULT"]["mqtt_port"])

    # Mqtt
    transport.connect_transport(mqtt_user, mqtt_pass, mqtt_server, mqtt_port)
    transport.register_callback(message_received)

    logger.info("Starting service")
    transport.send_message("doorbell mqtt started")

    pause()

    transport.stop_transport()


if __name__ == "__main__":
    main(sys.argv[1:])
