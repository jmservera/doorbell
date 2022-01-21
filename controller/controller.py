#!/usr/bin/python3
# Uses edge detection to limit the rate of Mqtt-messages

import paho.mqtt.client as paho
import time
import RPi.GPIO as GPIO
import sys


from signal import pause

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mqttc = None

formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

import configparser


def sendmqtt(mess):
    topic="doorbell/ding"
    try:
        logger.info("Message '"+mess+"' to "+topic)
        mqttc.publish(topic, mess)
    except:
        logger.error("mqtt error")
        logger.error(sys.exc_info()[1])
        pass


def mqttConnect(mqtt_user,mqtt_pass,mqtt_server,mqtt_port):
    logger.info("MQTT trying connection to "+mqtt_server+":"+str(mqtt_port))

    mqttc = paho.Client()
    mqttc.username_pw_set(mqtt_user, mqtt_pass)

    mqttc.connect(mqtt_server,mqtt_port)

    logger.info("MQTT configured")

    return mqttc

def ring_callback(channel):
    logger.info('Fall detected')
    sendmqtt("on")
    time.sleep(5)
    sendmqtt("off")

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
    mqttc = mqttConnect(mqtt_user,mqtt_pass,mqtt_server,mqtt_port)


    # Setup Gpio
    #GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input_pin, GPIO.IN)          # Output from Doorbell
    GPIO.setup(output_pin,GPIO.OUT)         # Open door relay

    logger.info("GPI configured in pin: "+str(input_pin))


    logger.info("Starting service")
    sendmqtt("doorbell mqtt started")

    GPIO.add_event_detect(input_pin, GPIO.FALLING, callback=ring_callback)
    pause()

if __name__ == "__main__":
    main(sys.argv[1:])
