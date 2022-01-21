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

def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning("Unexpected MQTT disconnection. Will auto-reconnect")

def on_connect(client, userdata, flags, rc):
    if rc==0:
        logger.info("MQTT connected OK Returned code=" + str(rc))
        mqttc.subscribe("doorbell/#",1)
        logger.info("Subscribed to doorbell messages")
    else:
        logger.error("MQTT Bad connection Returned code=" + str(rc))

def on_message(client, userdata, message):
    logger.warning("Message arrived: " + message.topic + " '" + message.payload.decode() + "'")


def mqttConnect(mqtt_user,mqtt_pass,mqtt_server,mqtt_port):
    logger.info("MQTT trying connection to "+mqtt_server+":"+str(mqtt_port))

    mqttc = paho.Client()
    mqttc.username_pw_set(mqtt_user, mqtt_pass)

    mqttc.connect(mqtt_server,mqtt_port)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_disconnect = on_disconnect
    mqttc.loop_start()

    logger.info("MQTT configured")

    return mqttc

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
                sendmqtt("{ \"on\": "+str(ring_count)+" }")
                time.sleep(5)
                sendmqtt("off")
            else:
                logger.info("loop")
        finally:
            ring_running = False
    else:
        logger.info("overlap")
    logger.info("Ring: "+str(ring_count))



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
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)          # Output from Doorbell
    GPIO.setup(output_pin,GPIO.OUT)         # Open door relay

    logger.info("GPI configured in pin: "+str(input_pin))


    logger.info("Starting service")
    sendmqtt("doorbell mqtt started")

    GPIO.add_event_detect(input_pin, GPIO.FALLING, callback=ring_callback)
    pause()

    mqttc.loop_stop()

if __name__ == "__main__":
    main(sys.argv[1:])
