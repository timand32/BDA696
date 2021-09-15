"""Module for loading and describing the Iris data set from the web.
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
        logging.Logger: [description]

    Todo:
        Put this in its own module, eventually in shared library between apps.
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


def main() -> int:
    # Setup logger with a helper function
    logger = create_logger(
        log_name="iris.data", log_level=logging.DEBUG, use_file_handler=True
    )
    logger.info("Loading Iris data set.")
    logger.info("Loading Iris metadata.")
    logger.info("Describing Iris data set.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
