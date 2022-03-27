import configparser
from typing import Callable
import RPi.GPIO as GPIO
import time
from . import logger

output_pin = None


def open_door() -> None:
    GPIO.output(output_pin, 1)
    time.sleep(0.5)
    GPIO.output(output_pin, 0)


def init_pi(
    config: configparser.ConfigParser, ring_callback: Callable[[int], None]
) -> None:
    global output_pin

    input_pin = int(config["DEFAULT"]["input_pin"])
    output_pin = int(config["DEFAULT"]["output_pin"])

    # Setup Gpio
    # GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    # Output from Doorbell
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Open door relay
    GPIO.setup(output_pin, GPIO.OUT)

    logger.info("GPI configured in pin: " + str(input_pin))

    GPIO.add_event_detect(input_pin, GPIO.FALLING, callback=ring_callback)
