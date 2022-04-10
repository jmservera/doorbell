import configparser
from abc import ABC, abstractmethod
from typing import Callable


class rpi_interface(ABC):
    @abstractmethod
    def open_door(self) -> None:
        pass

    @abstractmethod
    def __init__(
        self,
        config: configparser.ConfigParser,
        ring_callback: Callable[[int], None],
    ) -> None:
        pass
