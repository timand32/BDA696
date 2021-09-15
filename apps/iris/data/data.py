"""Module for loading and describing the Iris data set from the web.
"""
import logging
import os
import sys

import pandas as pd

feature_dict = {
    0: "sepal_length",
    1: "sepal_width",
    2: "pedal_length",
    3: "pedal_width",
    4: "class",
}

_mrsharky_data_path = "https://teaching.mrsharky.com/data/iris.data"


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


def load_data(data_path=_mrsharky_data_path) -> pd.DataFrame:
    """Loads Iris data set and returns a pandas DataFrame.

    Adds column names to the DataFrame.

    Args:
        data_path (str, optional): Path to download a .csv of Iris data.
        Defaults to "https://teaching.mrsharky.com/data/iris.data".

    Returns:
        pd.DataFrame: A pandas DataFrame containing the Iris data set.
    """
    df = pd.read_csv(data_path, header=None)
    df = df.rename(columns=feature_dict)
    return df


def describe_data(data_df: pd.DataFrame) -> pd.DataFrame:
    pass


def main() -> int:
    # Setup logger with a helper function
    logger = create_logger(
        log_name="iris.data", log_level=logging.DEBUG, use_file_handler=True
    )
    logger.info("Loading Iris data set.")
    data_df = load_data()
    print(data_df)
    logger.info("Describing Iris data set.")
    desc_df = describe_data(data_df=data_df)
    print(desc_df)
    return 0


if __name__ == "__main__":
    sys.exit(main())
