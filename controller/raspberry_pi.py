import configparser
import time
from typing import Callable

import RPi.GPIO as GPIO  # type: ignore

from . import interfaces, logger


class rpi(interfaces.rpi_interface):

    _output_pin = None

    def open_door(self) -> None:
        GPIO.output(self._output_pin, 1)
        time.sleep(0.5)
        GPIO.output(self._output_pin, 0)

    def __init__(
        self,
        config: configparser.ConfigParser,
        ring_callback: Callable[[int], None],
    ) -> None:

        input_pin = int(config["DEFAULT"]["input_pin"])
        self._output_pin = int(config["DEFAULT"]["output_pin"])

        # Setup Gpio
        # GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # Output from Doorbell
        GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Open door relay
        GPIO.setup(self._output_pin, GPIO.OUT)

        logger.info("GPI configured in pin: " + str(input_pin))

        GPIO.add_event_detect(input_pin, GPIO.FALLING, callback=ring_callback)
