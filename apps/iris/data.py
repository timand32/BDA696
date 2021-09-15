"""Module for loading and describing the Iris data set from the web.
"""
import logging
import sys

import log
import numpy as np
import pandas as pd

feature_dict = {
    0: "sepal_length",
    1: "sepal_width",
    2: "pedal_length",
    3: "pedal_width",
    4: "class",
}
"A dict of feature names."

continuous_feature_list = [feature_dict[i] for i in range(0, 4)]
"A list of continuous feature names."

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
"A dict of desired descriptive stats and their numpy function."

_mrsharky_data_path = "https://teaching.mrsharky.com/data/iris.data"


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


def _describe_feature(
    data_df: pd.DataFrame, desc_df: pd.DataFrame, feature: "str"
) -> pd.DataFrame:
    """Appends descriptive stats for a given feature in the Iris dataset.

    Args:
        data_df (pd.DataFrame): DataFrame of Iris dataset.
        desc_df (pd.DataFrame): DataFrame of descriptive statistics.

    Returns:
        pd.DataFrame: The appended description DataFrame.
    """
    # Build a list for the new row.
    row_list = [feature]
    # For each stat defined in this module,
    # run its associated numpy function.
    for stat in stat_dict:
        stat_value = data_df[feature]
        row_list.append(stat_dict[stat](stat_value))
    # Turn it into a series and append it to the df.
    column_names = ["feature"] + list(stat_dict)
    print(f"{column_names}\n{row_list}")
    row_srs = pd.Series(row_list, index=column_names)
    desc_df = desc_df.append(row_srs, ignore_index=True)
    return desc_df


def describe_data(data_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates descriptive stats and returns a pandas DataFrame.

    Args:
        data_df (pd.DataFrame): A pandas DataFrame of the Iris data set.

    Returns:
        pd.DataFrame: Data frame with descriptive stats of each feature.
    """
    desc_df = pd.DataFrame()
    features = continuous_feature_list
    for feature in features:
        desc_df = _describe_feature(data_df, desc_df, feature)
    desc_df = desc_df.set_index(["feature"])
    return desc_df


def main() -> int:
    # Setup logger with a helper function
    logger = log.create_logger(
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
