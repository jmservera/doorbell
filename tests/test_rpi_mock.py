from controller.rpi_mock import rpi
import configparser


ring_fired = False


def ring_handler(s):
    global ring_fired
    ring_fired = True


def test_rpi_ring():
    """Test the rpi ring event"""
    global ring_fired

    ring_fired = False
    rpi_test = rpi(configparser.ConfigParser())
    rpi_test.ring_event += ring_handler
    rpi_test.ring_callback()
    assert ring_fired


ring_fired_times = 0


def ring_handler_sum(s):
    global ring_fired_times
    ring_fired_times += 1


def test_rpi_multiple_ring():
    """Test the rpi ring event with multiple subscribers"""
    global ring_fired_times

    ring_fired_times = 0
    rpi_test = rpi(configparser.ConfigParser())
    rpi_test.ring_event += ring_handler_sum
    rpi_test.ring_event += ring_handler_sum
    rpi_test.ring_callback()
    assert ring_fired_times == 2

    rpi_test.ring_event -= ring_handler_sum
    rpi_test.ring_callback()
    assert ring_fired_times == 3
