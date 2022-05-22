from .mocks import mock_pi

# import source.module as mod
# import tests.helpers as hlp
import controller
import controller.doorbell


def test_module_func():
    assert True


def test_controller():
    assert controller.__version__ == "0.1.0a0"


def test_doorbell_open():
    _pi = mock_pi(None, None)
    door = controller.doorbell.doorbell(_pi)
    door.Open()
    assert _pi.openCalled
