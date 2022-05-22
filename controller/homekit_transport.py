import signal
import sys
import uuid

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_DOOR

from . import interfaces, logger


class RingSensor(Accessory):
    """Implementation of the Doorbell Ring Sensor"""

    category = CATEGORY_DOOR

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Add the services that this Accessory will support with
        # add_preload_service here
        ring_service = self.add_preload_service("RingSensor")
        self.char_detected = ring_service.configure_char("RingDetected")

    def Ring(self):
        self.char_detected.set_value(True)


class homekit_transport(interfaces.transport_interface):
    """The Homekit transport class"""

    _bridge: Bridge
    _ring: RingSensor
    _driver: AccessoryDriver
    _name: str

    def __init__(self, name: str):
        self._name = name
        pass

    def send_message(self, mess: str) -> None:
        """Send a message to the Homekit broker"""
        topic = "doorbell/ding"
        try:
            logger.info("Message '" + mess + "' to " + topic)
            self._ring.Ring()
        except (ValueError, TypeError):
            logger.error("mqtt error")
            logger.error(sys.exc_info()[1])
            pass

    def _get_bridge(self):
        """Call this method to get a Bridge."""
        self._bridge = Bridge(display_name="Bridge")

        id = uuid.getnode()
        self._ring = RingSensor(
            display_name=self._name + "RingSensor", id=1 + id * 10
        )
        self._bridge.add_accessory(self._ring)

        return self._bridge

    def connect_transport(self):
        """Connect to the broker"""
        acc = self._get_bridge()
        # Start the accessory on port 51826
        self._driver = AccessoryDriver(acc, port=51826)
        # We want KeyboardInterrupts and SIGTERM (kill) to be handled by the
        # driver itself, so that it can gracefully stop the accessory, server
        # and advertising.
        signal.signal(signal.SIGINT, self._driver.signal_handler)
        signal.signal(signal.SIGTERM, self._driver.signal_handler)
        # Start it!
        self._driver.start()

    def stop_transport(self):
        """Stop the transport"""
        logger.info("Stopping transport")
        self._driver.stop()
