import configparser
from typing import Callable
from controller.interfaces import rpi_interface


class mock_pi(rpi_interface):
    openCalled: bool = False

    def open_door(self) -> None:
        self.openCalled = True
        pass

    def __init__(
        self,
        config: configparser.ConfigParser,
        ring_callback: Callable[[int], None],
    ) -> None:
        pass
