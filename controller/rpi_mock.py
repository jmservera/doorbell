import configparser

from . import interfaces, logger


class rpi(interfaces.rpi_interface):
    def open_door(self) -> bool:
        logger.info("Opening door")
        return True

    def __init__(self, config: configparser.ConfigParser) -> None:
        super().__init__(config)

    def ring_callback(self) -> None:
        self._event("ring")
