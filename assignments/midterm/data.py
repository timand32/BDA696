"""Module imports test data.

Adapted almost fully from the hw4_data.py script given in class,
with the following changes:
0. Moved the first few declarations into module 'constants'.
1. I also made a `get_all_test_data_sets()` function.
2. My IDE was complaining at including paretheses in the return type,
so I used List[x,y,z] instead from the typing module.
3. Edited docstrings to use NumPy style docstrings.
This particularly looks nice in my IDE,
hopefully PyCharm also does some formatting.
4. Changed error type to ValueError.
5. Removed .dropna() from the seaborn datasets,
as I wanted to try handling them in my system.
6. I removed the Boston data set.
The scikit-learn maintainers deprecated it and plan to remove it soon.
"""
import random
import sys
from typing import Dict, List, Tuple

import numpy
import pandas  # type: ignore
import seaborn  # type: ignore
from sklearn import datasets  # type: ignore

SEABORN_DATA_SETS = ["mpg", "tips", "titanic"]
"""Names of supported seaborn data sets."""
SKLEARN_DATA_SETS = ["diabetes", "breast_cancer"]
"""Names of supported scikit-learn data sets."""
ALL_DATA_SETS = SEABORN_DATA_SETS + SKLEARN_DATA_SETS
"""Names of all supported data sets."""


def get_test_data_set(
    data_set_name: str = None,
) -> Tuple[pandas.DataFrame, List[str], str]:
    """Function to load a few test data sets.

    Parameters:
    -----------
    data_set_name (str, optional):
        Data set to load. Defaults to None.

    Raises:
    -------
    ValueError:
        if data_set_name is not an included data set.

    Returns:
    --------
    Tuple[pandas.DataFrame, List[str], str]:
        A tuple containing the data set,
        a list of predictors in the data set,
        and the target response variable in the data.
    """
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
    return data_set, predictors, response


def get_all_test_data_sets() -> Dict[
    str,
    Tuple[pandas.DataFrame, List[str], str],
]:
    """Function to load all test data sets into a dict.

    Returns:
    --------
    Dict[str, Tuple[pandas.DataFrame, List[str], str]]:
        A str indexed dict of tuples containing the data set,
        a list of predictors in the data set,
        and the target response variable in the data.
    response: `str`
        Response variable
    """
    data_set_dict = dict()
    for data_set in ALL_DATA_SETS:
        data_set_dict[data_set] = get_test_data_set(data_set)
    return data_set_dict


def main() -> int:
    data_set_dict = get_all_test_data_sets()
    for name, data_set in data_set_dict.items():
        df, predictors, response = data_set
        print(f"Set Name: {name}")
        print(f"Predictors: {predictors}")
        print(f"Response: {response}")
        print(f"DataFrame:\n{df}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
