"""Define function for loading test datasets.

Adapted from the hw4_data.py script given in class.
"""
import random
import sys

import numpy
import pandas  # type: ignore
import seaborn  # type: ignore
from dataset import Dataset
from sklearn import datasets  # type: ignore

SEABORN_DATA_SETS = ["mpg", "tips", "titanic"]
"""Names of supported seaborn data sets."""
SKLEARN_DATA_SETS = ["diabetes", "breast_cancer"]
"""Names of supported scikit-learn data sets."""
ALL_DATA_SETS = SEABORN_DATA_SETS + SKLEARN_DATA_SETS
"""Names of all supported data sets."""


def get_dataset(
    data_set_name: str = None,
) -> Dataset:
    if data_set_name is None:
        data_set_name = random.choice(ALL_DATA_SETS)
    else:
        if data_set_name not in ALL_DATA_SETS:
            raise ValueError(f"Data set choice not valid: {data_set_name}")

    if data_set_name in SEABORN_DATA_SETS:
        if data_set_name == "mpg":
            data_set = seaborn.load_dataset(name="mpg").reset_index()
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
            data_set = seaborn.load_dataset(name="tips").reset_index()
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
            data_set = seaborn.load_dataset(name="titanic")
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


def main() -> int:
    dataset = get_dataset()
    print("Response type:\n", dataset.y_type)
    print("Response:\n", dataset.y)
    print("Predictors:\n", dataset.X)
    print("Categorical:\n", dataset.categorical_X)
    print("Continuous:\n", dataset.continuous_X)
    print("Combinations:\n", dataset.X_combinations)
    print(
        "Combinations:\n",
        dataset.get_combination_X(
            dataset.X_combinations["continuous", "continuous"][0]
        ),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
