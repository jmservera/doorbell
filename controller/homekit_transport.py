import signal
import sys
from asyncio import AbstractEventLoop, new_event_loop
from threading import Thread

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
        ring_service = self.add_preload_service("Doorbell")
        self.char_detected = ring_service.configure_char(
            "ProgrammableSwitchEvent", setter_callback=self._ring
        )
        self.setter_callback = self._ring

    def Ring(self):
        self.char_detected.set_value(True)

    def _ring(self, value):
        logger.info("Ring")


class homekit_transport(interfaces.transport_interface):
    """The Homekit transport class"""

    _bridge: Bridge
    _ring_sensor: RingSensor
    _driver: AccessoryDriver
    _name: str
    _loop: AbstractEventLoop
    _background_thread: Thread

    def __init__(self, name: str):
        self._name = name
        self._loop = new_event_loop()
        pass

    def send_message(self, mess: str) -> None:
        """Send a message to the Homekit broker"""
        topic = "doorbell/ding"
        try:
            logger.info("Message '" + mess + "' to " + topic)
            self._loop.call_soon_threadsafe(self._ring_sensor.Ring)
        except (ValueError, TypeError):
            logger.error("mqtt error")
            logger.error(sys.exc_info()[1])
            pass

    def _button_pressed(self, value):
        """Send a message to the Homekit broker"""
        logger.info("Bridge button pressed")
        self._ring_sensor.Ring()

    def _get_bridge(self):
        """Call this method to get a Bridge."""
        self._bridge = Bridge(
            self._driver, display_name=self._name + " Bridge"
        )
        self._bridge.setter_callback = self._button_pressed

        self._ring_sensor = RingSensor(
            self._driver, display_name=self._name + " Ring Sensor"
        )

        self._bridge.add_accessory(self._ring_sensor)

        return self._bridge

    def connect_transport(self):
        """Connect to the broker"""
        # Start the accessory on port 51826
        self._driver = AccessoryDriver(port=51826, loop=self._loop)
        self._driver.add_accessory(accessory=self._get_bridge())
        # We want KeyboardInterrupts and SIGTERM (kill) to be handled by the
        # driver itself, so that it can gracefully stop the accessory, server
        # and advertising.
        signal.signal(signal.SIGINT, self._driver.signal_handler)
        signal.signal(signal.SIGTERM, self._driver.signal_handler)
        # Start it!
        # self._driver.start()
        self._background_thread = Thread(target=self._driver.start)
        self._background_thread.start()

    def stop_transport(self):
        """Stop the transport"""
        logger.info("Stopping transport: " + self.__class__.__name__)

        self._loop.call_soon_threadsafe(self._loop.stop)
        self._background_thread.join()
        # self._driver.stop()
