"""Module with logging helper function.
"""
import logging
import os
import sys


def create_logger(
    log_name: str = __name__,
    log_level: int = logging.DEBUG,
    use_file_handler: bool = False,
) -> logging.Logger:
    """Configure and return a Python Logger object.

    Args:
        log_name  (str, optional): Sets new log's name.
        Defaults to __name__.
        log_level (int, optional): Sets logging level.
        Defaults to logging.DEBUG.
        use_file_handler (bool, optional): Adds a file handler if True.
        Defaults to False.

    Returns:
        logging.Logger: A configured Python Logger object.

    """
    logger = logging.getLogger(name=__name__)
    logger.setLevel(level=log_level)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(stream_handler)
    if use_file_handler is True:
        # Guarantee logs folder exists: from question 273192 on Stack Overflow.
        if not os.path.exists("./logs/"):
            os.makedirs("logs")
        handler_path = "./logs/" + log_name + ".log"
        file_handler = logging.FileHandler(handler_path)
        logger.addHandler(file_handler)
    return logger
