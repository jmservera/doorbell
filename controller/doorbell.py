from . import interfaces, logger


class doorbell(object):
    """This is the main doorbell class"""
    _rpi: interfaces.rpi_interface
    _last_ring = None
    _ring_count = 0

    def __init__(self, rpi: interfaces.rpi_interface) -> None:
        self._rpi = rpi
        pass

    def Open(self) -> None:
        self._rpi.open_door()
        pass


if __name__ == "doorbell":
    logger.info("Start doorbell")
