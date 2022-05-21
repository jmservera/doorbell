import configparser
from abc import ABC, abstractmethod
from typing import Any, Callable


class rpi_interface(ABC):
    """The Raspberry Pi interface"""
    @abstractmethod
    def open_door(self) -> None:
        """Activates the open door mecanism"""
        pass

    @abstractmethod
    def __init__(
        self,
        config: configparser.ConfigParser,
        ring_callback: Callable[[int], None],
    ) -> None:
        """Initializes the Raspberry Pi interface"""
        pass


class transport_interface(ABC):
    """The Transport interface for external input/output messaging"""
    _message_callback: Callable[[str, Any], None]

    @property
    def on_message(self) -> Callable[[str, Any], None]:
        """Get or set the callback function for MQTT messages"""
        return self._message_callback

    @on_message.setter
    def on_message(self, callback: Callable[[str, Any], None]) -> None:
        """Get or set the callback function for MQTT messages"""
        self._message_callback = callback

    @abstractmethod
    def send_message(self, mess: str) -> None:
        """Send a message to the client"""
        pass
