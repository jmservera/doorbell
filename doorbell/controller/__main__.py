#!/usr/bin/python3
# Uses edge detection to limit the rate of Mqtt-messages
import sys

import time
import RPi.GPIO as GPIO

from signal import pause

from logger import logger
import transport

import configparser

ring_running = False
ring_count = 0

def ring_callback(channel):
    global ring_running, ring_count

    ring_count = ring_count + 1 
    if not ring_running:
        ring_running = True
        try:
            if channel:
                logger.info('Fall detected')
                transport.send_message("{ \"on\": "+str(ring_count)+" }")
                time.sleep(5)
                transport.send_message("off")
            else:
                logger.info("loop")
        finally:
            ring_running = False
    else:
        logger.info("overlap")
    logger.info("Ring: "+str(ring_count))

def message_received(topic, message):
    logger.info(topic + str(message))


def main(argv):

    global mqttc, mqtt_server, mqtt_port

    config = configparser.ConfigParser()
    config.read('config.ini')

    input_pin=int(config['DEFAULT']['input_pin'])
    output_pin=int(config['DEFAULT']['output_pin'])
    mqtt_user=config['DEFAULT']['mqtt_user']
    mqtt_pass=config['DEFAULT']['mqtt_pass']
    mqtt_server=config['DEFAULT']['mqtt_server']
    mqtt_port=int(config['DEFAULT']['mqtt_port'])


    # Mqtt
    transport.connect_transport(mqtt_user,mqtt_pass,mqtt_server,mqtt_port)
    transport.register_callback(message_received)


    # Setup Gpio
    #GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)          # Output from Doorbell
    GPIO.setup(output_pin,GPIO.OUT)         # Open door relay

    logger.info("GPI configured in pin: " + str(input_pin))


    logger.info("Starting service")
    transport.send_message("doorbell mqtt started")

    GPIO.add_event_detect(input_pin, GPIO.FALLING, callback=ring_callback)

    GPIO.output(output_pin, 1)
    logger.info("pin 1")
    time.sleep(5)
    GPIO.output(output_pin, 0)
    logger.info("pin 0")

    pause()

    transport.stop_transport()

if __name__ == "__main__":
    main(sys.argv[1:])
