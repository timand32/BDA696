"""Module for loading and describing the Iris data set from the web.
"""
import logging
import os
import sys

import numpy as np
import pandas as pd

"Dictionary of feature names."
feature_dict = {
    0: "sepal_length",
    1: "sepal_width",
    2: "pedal_length",
    3: "pedal_width",
    4: "class",
}

"Dictionary of desired descriptive stats and their np function."
stat_dict = {
    "count": np.count_nonzero,
    "mean": np.mean,
    "std_dv.": np.std,
    "min": np.min,
    "max": np.max,
    "q1": lambda x: np.quantile(x, 0.25),
    "q2": lambda x: np.quantile(x, 0.50),
    "q3": lambda x: np.quantile(x, 0.75),
    "q4": lambda x: np.quantile(x, 1.0),
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
    """Calculates descriptive stats and returns a pandas DataFrame.

    Args:
        data_df (pd.DataFrame): A pandas DataFrame of the Iris data set.

    Returns:
        pd.DataFrame: Data frame with descriptive stats of each feature.
    """
    desc_df = pd.DataFrame()
    features = [feature_dict[i] for i in range(0, 4)]
    for feature in features:
        # Build a list for the new row.
        row_list = [
            feature,
        ]
        for stat in stat_dict:
            stat_value = data_df[feature]
            row_list.append(stat_dict[stat](stat_value))
        column_names = [
            "feature",
        ] + list(stat_dict)
        row_srs = pd.Series(row_list, index=column_names)
        desc_df = desc_df.append(row_srs, ignore_index=True)
    desc_df = desc_df.set_index(["feature"])
    return desc_df


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
