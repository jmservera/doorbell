import configparser
import importlib
from typing import Any, Callable

from . import logger
from .interfaces import rpi_interface


def dynamic_imp(name, class_name) -> Any:
    myclass = Any
    try:
        mod = importlib.import_module(name, "controller")
        try:
            myclass = mod.__dict__[class_name]
        except Exception as e:
            logger.error("class not found: " + class_name, exc_info=e)
    except ImportError as e:
        logger.error("module not found: " + name, exc_info=e)

    return myclass


def load_pi(
    config: configparser.ConfigParser, ring_callback: Callable[[int], None]
) -> rpi_interface:
    """Load the Raspberry Pi interface"""
    # dynamic import
    if config.getboolean("DEFAULT", "rpi_mock"):
        myclass = dynamic_imp(".rpi_mock", "rpi")
        return myclass(config, ring_callback)
    else:
        myclass = dynamic_imp(".raspberry_pi", "rpi")
        return myclass.rpi(config, ring_callback)
