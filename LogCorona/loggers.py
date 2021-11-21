import logging
from typing import Any


def init_logger() -> Any:
    # The basic of the Code is from Logging HOWTO website that create a logger and stream handler
    # to print the log to console
    # https://docs.python.org/3/howto/logging.html
    # By Vinay Sajip
    logger = logging.getLogger('log_corona_logger')
    logger.setLevel(logging.DEBUG)
    stream_logging_handler = logging.StreamHandler()
    stream_logging_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_logging_handler.setFormatter(formatter)
    logger.addHandler(stream_logging_handler)
    return logger
