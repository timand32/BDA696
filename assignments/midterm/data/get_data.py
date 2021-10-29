"""Define function for loading test datasets.

Adapted from the hw4_data.py script given in class.
"""
import random

import numpy
import pandas  # type: ignore
import seaborn  # type: ignore
from sklearn import datasets  # type: ignore

from . import Dataset

SEABORN_DATA_SETS = ["mpg", "tips", "titanic"]
"""Names of supported seaborn data sets."""
SKLEARN_DATA_SETS = ["diabetes", "breast_cancer", "boston"]
"""Names of supported scikit-learn data sets."""
ALL_DATA_SETS = SEABORN_DATA_SETS + SKLEARN_DATA_SETS
"""Names of all supported data sets."""


def get_dataset(
    data_set_name: str = None,
) -> Dataset:
    """Get a test dataset from either seaborn's or scikit's collection.

    Args:
        data_set_name (str, optional):
            Name of dataset. Defaults to None.

    Raises:
        ValueError:
            Raised if no dataset exists with a given name.

    Returns:
        Dataset:
            A Dataset object based on a DataFrame or numpy dataset.
    """
    if data_set_name is None:
        data_set_name = random.choice(ALL_DATA_SETS)
    else:
        if data_set_name not in ALL_DATA_SETS:
            raise ValueError(f"Data set choice not valid: {data_set_name}")

    if data_set_name in SEABORN_DATA_SETS:
        if data_set_name == "mpg":
            data_set = seaborn.load_dataset(name="mpg").dropna().reset_index()
            predictors = [
                "cylinders",
                "displacement",
                "horsepower",
                "weight",
                "acceleration",
                "origin",
            ]
            response = "mpg"
        elif data_set_name == "tips":
            data_set = seaborn.load_dataset(name="tips").dropna().reset_index()
            predictors = [
                "total_bill",
                "sex",
                "smoker",
                "day",
                "time",
                "size",
            ]
            response = "tip"
        elif data_set_name == "titanic":
            data_set = seaborn.load_dataset(name="titanic").dropna()
            data_set = data_set.reset_index()
            predictors = [
                "pclass",
                "sex",
                "age",
                "sibsp",
                "embarked",
                "class",
            ]
            response = "survived"
    elif data_set_name in SKLEARN_DATA_SETS:
        if data_set_name == "diabetes":
            data = datasets.load_diabetes()
            data_set = pandas.DataFrame(data.data, columns=data.feature_names)
        elif data_set_name == "breast_cancer":
            data = datasets.load_breast_cancer()
            data_set = pandas.DataFrame(data.data, columns=data.feature_names)
        elif data_set_name == "boston":
            data = datasets.load_boston()
            data_set = pandas.DataFrame(data.data, columns=data.feature_names)
        data_set["target"] = data.target
        predictors = data.feature_names
        if type(predictors) == numpy.ndarray:
            # Make sure we get a list in the end.
            predictors = predictors.tolist()
        response = "target"
    return Dataset(
        title=data_set_name,
        df=data_set,
        predictor_columns=predictors,
        response_column=response,
    )
