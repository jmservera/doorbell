import configparser
from abc import ABC, abstractmethod
from typing import Any, Callable


class Event(object):
    def __init__(self):
        self.__eventhandlers = []

    def __iadd__(self, handler):
        self.__eventhandlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__eventhandlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)


class rpi_interface(ABC):
    """The Raspberry Pi interface"""

    @abstractmethod
    def open_door(self) -> bool:
        """Activates the open door mecanism"""
        pass

    def __init__(self, config: configparser.ConfigParser) -> None:
        """Initializes the Raspberry Pi interface"""
        self._event = Event()

    @property
    def ring_event(self):
        return self._event

    @ring_event.setter
    def ring_event(self, ring_handler: Event) -> None:
        """Get or set the callback function for received messages"""
        self._event = ring_handler


class transport_interface(ABC):
    """The Transport interface for external input/output messaging"""

    _message_callback: Callable[[str, Any], None]

    # TODO: change methods for explicit ones
    # emit_ring
    # on_open_received

    @property
    def on_message(self) -> Callable[[str, Any], None]:
        """Get or set the callback function for received messages"""
        return self._message_callback

    @on_message.setter
    def on_message(self, callback: Callable[[str, Any], None]) -> None:
        """Get or set the callback function for received messages"""
        self._message_callback = callback

    @abstractmethod
    def send_message(self, mess: str) -> None:
        """Send a message to the client"""
        pass

    @abstractmethod
    def stop_transport(self) -> None:
        """Stop the transport"""
        pass
