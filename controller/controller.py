#!/usr/bin/python3
# Uses edge detection to limit the rate of Mqtt-messages

import paho.mqtt.client as paho
import time
import urllib.parse
import RPi.GPIO as GPIO
import datetime
import sys

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mqttc = None

formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

import configparser


def printtime(): # Used for debug
    # Current time
    global hour, minute, wholetime
    now = datetime.datetime.now()
    hour = str(now.hour)
    minute = int(now.minute)
    minute = '%02d' % minute
    wholetime = hour + ":" + minute

def sendmqtt(mess):
    topic="doorbell/ding"
    try:
        logger.info("Message '"+mess+"' to "+topic)
        mqttc.publish(topic, mess)
    except:
        logger.error("mqtt error")
        logger.error(sys.exc_info()[1])
        pass


def mqttConnect(mqtt_user,mqtt_pass):
    logger.info("MQTT trying connection to "+mqtt_server+":"+str(mqtt_port))

    mqttc = paho.Client()
    mqttc.username_pw_set(mqtt_user, mqtt_pass)

    mqttc.connect(mqtt_server,mqtt_port)

    logger.info("MQTT configured")

    return mqttc

def main(argv):

    global mqttc, mqtt_server, mqtt_port

    count=0

    config = configparser.ConfigParser()
    config.read('config.ini')

    input_pin=int(config['DEFAULT']['input_pin'])
    output_pin=int(config['DEFAULT']['output_pin'])
    mqtt_user=config['DEFAULT']['mqtt_user']
    mqtt_pass=config['DEFAULT']['mqtt_pass']
    mqtt_server=config['DEFAULT']['mqtt_server']
    mqtt_port=int(config['DEFAULT']['mqtt_port'])


    # Mqtt
    mqttc = mqttConnect(mqtt_user,mqtt_pass)


    # Setup Gpio
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input_pin, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)         # Output from Doorbell

    logger.info("GPI configured in pin: "+str(input_pin))


    logger.info("Starting service")
    sendmqtt("doorbell mqtt started")

    while True:
        try:
            channel=GPIO.wait_for_edge(input_pin, GPIO.FALLING, timeout=5000)
            if channel is None:
                count=count+1
                if count>25:
                    count=0
                    sendmqtt("alive")
                logger.info('Loop')
            else:
                logger.info('Fall detected')
                sendmqtt("on")
                time.sleep(5)
                sendmqtt("off")
        except KeyboardInterrupt:
            # quit
            sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
