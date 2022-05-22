from controller.interfaces import rpi_interface

# import source.module as mod
# import tests.helpers as hlp
import controller
import controller.doorbell

from unittest.mock import MagicMock


def test_module_func():
    assert True


def test_controller():
    assert controller.__version__ == "0.1.0a0"


def test_doorbell_open():
    _pi = MagicMock(spec=rpi_interface)
    _pi.open_door = MagicMock(return_value=True)
    door = controller.doorbell.doorbell(_pi)
    assert door.Open()
