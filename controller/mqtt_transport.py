import sys

import paho.mqtt.client as paho

from . import interfaces, logger


class mqtt_transport(interfaces.transport_interface):
    """The MQTT transport class"""

    _mqttc = paho.Client()

    def __init__(self):
        pass

    def send_message(self, mess: str) -> None:
        """Send a message to the MQTT broker"""
        topic = "doorbell/ding"
        try:
            logger.info("Message '" + mess + "' to " + topic)
            self._mqttc.publish(topic, mess)
        except (ValueError, TypeError):
            logger.error("mqtt error")
            logger.error(sys.exc_info()[1])
            pass

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning(
                "Unexpected MQTT disconnection. Will auto-reconnect"
            )

    def _on_fail(self, client, userdata) -> None:
        logger.warning("MQTT connection failed")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("MQTT connected OK Returned code=" + str(rc))
            self._mqttc.subscribe("doorbell/#", 1)
            logger.info("Subscribed to doorbell messages")
        else:
            logger.error("MQTT Bad connection Returned code=" + str(rc))

    def _on_mqtt_message(self, client, userdata, message):

        logger.info("Message arrived" + message.topic)
        payload = message.payload.decode()
        logger.info("Payload: '" + payload + "'")
        if self._message_callback is not None:
            self._message_callback(message.topic, payload)
        else:
            logger.warning("Message lost. No message callback registered.")

    def connect_transport(
        self, mqtt_user: str, mqtt_pass: str, mqtt_server: str, mqtt_port: int
    ):
        """Connect to the MQTT broker"""
        logger.info(
            "MQTT trying connection to " + mqtt_server + ":" + str(mqtt_port)
        )
        self._mqttc.username_pw_set(mqtt_user, mqtt_pass)
        self._mqttc.connect(mqtt_server, mqtt_port)
        self._mqttc.on_connect = self._on_connect
        self._mqttc.on_message = self._on_mqtt_message
        self._mqttc.on_disconnect = self._on_disconnect
        self._mqttc.connect_fail_callback = self._on_fail
        self._mqttc.loop_start()

        logger.info("MQTT configured")

    def stop_transport(self):
        """Stop the MQTT transport"""
        logger.info("Stopping transport")
        self._mqttc.loop_stop()
