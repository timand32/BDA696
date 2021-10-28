import itertools
from typing import Dict, List, Optional, Tuple

import pandas


def determine_response_type(y: pandas.Series) -> str:
    """"""
    if len(y.unique()) == 2:
        return "boolean"
    else:
        return "continuous"


def determine_predictor_type(
    x: pandas.Series,
    categorical_threshold: float = 0.05,
) -> str:
    """"""
    # Assume category or object dtypes are categorical
    if x.dtype.name in ["category", "object"]:
        return "categorical"
    # Heuristic from Stack Overflow Q#35826912
    if float(x.nunique()) / x.count() < categorical_threshold:
        return "categorical"
    # Otherwise, we can assume its continuous
    return "continuous"


class Dataset(object):
    """Class for encapsulating a dataframe with other information.

    Main reason is that my function definitions were a mess without it.
    This tries to solve that problem,
    letting most analysis and plotting classes/functions to just need one,
    standard parameter.
    """

    def __init__(
        self,
        title: str,
        df: pandas.DataFrame,
        response_column: str,
        predictor_columns: List[str],
        categorical_threshold: float = 0.05,
    ):
        """Initialize a dataset, determining feature types and combinations.

        Args:
            title (str): Title for dataset.
            df (pandas.DataFrame):
                Data to add to dataset.
            response_column (str):
                Column in data frame to use as response.
            predictor_columns (List[str]):
                Columns to use as predictors.
            categorical_threshold (float, optional):
                Threshold for categorical heuristic.
                Heuristic is (unique values in X)/(size of X) < threshold.
                Defaults to 0.05.
        """
        self.__title = title
        self.__y: pandas.Series = df[response_column]
        self.__y_type: str = determine_response_type(self.__y)
        self.__X: pandas.DataFrame = df[predictor_columns]
        categorical_columns = [
            x.name
            for _, x in self.__X.items()
            if determine_predictor_type(
                x,
                categorical_threshold,
            )
            == "categorical"
        ]
        self.__categorical_X: pandas.DataFrame = self.__X[categorical_columns]
        continuous_columns = [
            x.name
            for _, x in self.__X.items()
            if determine_predictor_type(x) == "continuous"
        ]
        self.__continuous_X: pandas.DataFrame = self.__X[continuous_columns]
        cat_cat_combinations = itertools.combinations(
            self.categorical_X.columns,
            r=2,
        )
        cat_cont_combinations = itertools.product(
            self.categorical_X.columns, self.continuous_X.columns, repeat=1
        )
        cont_cont_combinations = itertools.combinations(
            self.continuous_X.columns,
            r=2,
        )
        self.__X_combinations = {
            ("categorical", "categorical"): [c for c in cat_cat_combinations],
            ("categorical", "continuous"): [c for c in cat_cont_combinations],
            ("continuous", "continuous"): [c for c in cont_cont_combinations],
        }

    @property
    def title(self) -> str:
        """"""
        return self.__title

    @property
    def y(self) -> pandas.Series:
        """"""
        return self.__y

    @property
    def y_type(self) -> str:
        """"""
        return self.__y_type

    @property
    def X(self) -> pandas.DataFrame:
        """"""
        return self.__X

    @property
    def categorical_X(self) -> Optional[pandas.DataFrame]:
        """"""
        return self.__categorical_X

    @property
    def continuous_X(self) -> Optional[pandas.DataFrame]:
        """"""
        return self.__continuous_X

    @property
    def X_combinations(self) -> Dict[Tuple[str, str], List]:
        """"""
        return self.__X_combinations

    def get_combination_X(
        self,
        combination: Optional[Tuple[str, str]],
    ) -> pandas.DataFrame:
        """Get a pandas.DataFrame X based on a tuple of column names.
        You can access combinations from the property `X_combinations`.
        """
        a, b = combination
        return pandas.DataFrame(
            {
                a: self.X[a],
                b: self.X[b],
            }
        )
