import configparser
from typing import Callable

from . import interfaces, logger


class rpi(interfaces.rpi_interface):
    _ring_callback: Callable[[int], None]

    def open_door(self) -> bool:
        logger.info("Opening door")
        return True

    def __init__(
        self,
        config: configparser.ConfigParser,
        ring_callback: Callable[[int], None],
    ) -> None:
        self._ring_callback = ring_callback

    def ring_callback(self, channel: int) -> None:
        self._ring_callback(channel)
