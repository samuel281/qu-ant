import logging
import sys


def configure_logger(level=logging.INFO, formatter='%(levelname)s - %(message)s'):
    logging.basicConfig(stream=sys.stdout, level=level, format=formatter)