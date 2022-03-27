import sys
import logging

__version__ = "0.1.0a0"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Logger configured")
