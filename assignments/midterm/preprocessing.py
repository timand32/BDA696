"""Module defines preprocessing functions for pandas.DataFrame objects.
"""

import sys
from typing import List

import data
import pandas


def subset_dataframe(
    df: pandas.DataFrame,
    predictors: List[str],
    response: str,
) -> pandas.DataFrame:
    """[summary]

    Parameters:
    -----------
        df (pandas.DataFrame):
            A dataframe with response and predictor columns.
        predictors (List[str]):
            The predictor columns to add in the subset.
        response (str):
            The response column to add in the subset.

    Raises:
    -------
    ValueError:
        if predictors or response are not columns in the DataFrame.

    Returns:
    --------
        pandas.DataFrame:
            a DataFrame of the original's features
            including an 'is_response' column
            and a 'feature_type' column.
    """
    feature_list = predictors + [response]
    return df[feature_list]


def assign_response(
    features: pandas.Series,
    response: str,
) -> pandas.DataFrame:
    """Add a 'is_response' column based on column names.

    Parameters:
    -----------
        features (pandas.Series):
            A series containing feature names.
        response (str):
            The name of the feature to assign as response.

    Raises:
    -------
    ValueError:
        if response is not a column in the given DataFrame.

    Returns:
    --------
        pandas.DataFrame:
            a DataFrame including an 'is_response' column.
    """
    df = pandas.DataFrame()
    df["feature"] = features
    df["is_response"] = [True if f == response else False for f in features]
    return df


def determine_predictor_type(
    values: pandas.Series,
    categorical_threshhold: float,
) -> str:
    if values.dtype.name in ["category", "object"]:
        return "categorical"
    # Stack Overflow Q #35826912
    elif float(values.nunique()) / values.count() < categorical_threshhold:
        return "categorical"
    else:
        return "continuous"


def determine_response_type(
    values: pandas.Series,
) -> str:
    if len(values.unique()) == 2:
        return "boolean"
    else:
        return "continuous"


def determine_feature_types(
    df: pandas.DataFrame,
    response: str,
    categorical_threshold: float = 0.05,
) -> pandas.DataFrame:
    """Add a 'feature_type' and an 'is_response' column
    based on column values.

    Uses assign_response() in background
    (As processing for response/predictors is different).

    Parameters:
    -----------
        df (pandas.DataFrame):
            A dataframe with response and predictor columns.
        response (str):
            The name of the feature to assign as response.
        categorical_threshold (float, optional):
            Threshold parameter to use when determining categorical features.
            Defaults to 0.05.

    Raises:
    -------
    ValueError:
        if response is not a column in the given DataFrame.

    Returns:
    --------
        pandas.DataFrame:
            a DataFrame of the original's features
            including an 'is_response' column
            and a 'feature_type' column.
    """
    feat_series = pandas.Series(df.columns, name="feature")
    feat_df = assign_response(feat_series, response)
    feat_df["feature_type"] = "unknown"
    pred_loc = feat_df.loc[
        ~feat_df["is_response"],
        ["feature", "feature_type"],
    ]
    feat_df.loc[~feat_df["is_response"], ["feature_type"]] = [
        determine_predictor_type(df[p], categorical_threshold)
        for p in pred_loc["feature"]
    ]
    resp_loc = feat_df.loc[
        feat_df["is_response"],
        ["feature", "feature_type"],
    ]
    feat_df.loc[
        feat_df["is_response"],
        ["feature_type"],
    ] = [determine_response_type(df[p]) for p in resp_loc["feature"]]
    feat_df = feat_df.sort_values(by=["is_response", "feature_type"])
    return feat_df


def main() -> int:
    print("Subset DF:")
    df, predictors, response = data.get_test_data_set()
    sub_df = subset_dataframe(df, predictors, response)
    print(sub_df)
    print("'is_response' DF:")
    feat_series = pandas.Series(sub_df.columns, name="feature")
    resp_df = assign_response(feat_series, response)
    print(resp_df)
    print("Feature type DF:")
    feat_df = determine_feature_types(sub_df, response)
    print(feat_df)
    return 0


if __name__ == "__main__":
    sys.exit(main())
