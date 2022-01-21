import sys
from logger import logger
import paho.mqtt.client as paho

mqttc = None

def sendmqtt(mess):
    global mqttc
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
    global mqttc
    if rc==0:
        logger.info("MQTT connected OK Returned code=" + str(rc))
        mqttc.subscribe("doorbell/#",1)
        logger.info("Subscribed to doorbell messages")
    else:
        logger.error("MQTT Bad connection Returned code=" + str(rc))

def on_message(client, userdata, message):
    logger.warning("Message arrived: " + message.topic + " '" + message.payload.decode() + "'")


def mqttConnect(mqtt_user,mqtt_pass,mqtt_server,mqtt_port):
    global mqttc
    logger.info("MQTT trying connection to "+mqtt_server+":"+str(mqtt_port))

    mqttc = paho.Client()
    mqttc.username_pw_set(mqtt_user, mqtt_pass)

    mqttc.connect(mqtt_server,mqtt_port)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_disconnect = on_disconnect
    mqttc.loop_start()

    logger.info("MQTT configured")

def stop_transport():
    logger.info("Stopping transport")
    mqttc.loop_stop()

if __name__ == "transport":
    logger.info("Start transport")