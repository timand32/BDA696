"""Module implements difference with mean of response.

Reproduces formula and table given in class
"""

import sys

import data
import features
import pandas as pd


def calc_diff_with_mean_table_cont(
    df: pd.DataFrame,
    predictor: str,
    response: str,
    n: int = 10,
) -> pd.DataFrame:
    bin_df = pd.DataFrame()
    ps = df[predictor]
    rs = df[response]
    pred_df = ps.to_frame()
    pred_df[response] = rs
    pop_mean = rs.mean()
    # Based on lecture notes
    # Bin candidate predictor variable
    intervals = pd.qcut(ps, n)
    pred_df["LowerBin"] = pd.Series([i.left for i in intervals])
    pred_df["UpperBin"] = pd.Series([i.right for i in intervals])
    labels = ["LowerBin", "UpperBin"]
    bin_df["BinCenters"] = pred_df.groupby(by=labels).median()[predictor]
    bin_df["BinCount"] = pred_df.groupby(by=labels).count()[predictor]
    bin_df["Weight"] = bin_df["BinCount"] / ps.count()
    bin_df["BinMean"] = pred_df.groupby(by=labels).mean()[response]
    bin_df["PopulationMean"] = pop_mean
    # Compare the average value of response for the predictors in each bin
    msd = "MeanSquaredDiff"
    wmsd = "WeightedMeanSquaredDiff"
    bin_df[msd] = (bin_df["BinMean"] - bin_df["PopulationMean"]) ** 2
    bin_df[wmsd] = (
        bin_df["Weight"] * (bin_df["BinMean"] - bin_df["PopulationMean"]) ** 2
    )
    bin_df = bin_df.reset_index()
    return bin_df


def calc_diff_with_mean_table_cat(
    df: pd.DataFrame,
    predictor: str,
    response: str,
) -> pd.DataFrame:
    bin_df = pd.DataFrame()
    ps = df[predictor]
    rs = df[response]
    pred_df = ps.to_frame("Category")
    pred_df[response] = rs
    pop_mean = rs.mean()
    # Based on lecture notes
    # Bin candidate predictor variable
    # This time, just use categories.
    labels = ["Category"]
    bin_df["BinCount"] = pred_df.groupby(by=labels).count()[response]
    bin_df["Weight"] = bin_df["BinCount"] / ps.count()
    bin_df["BinMean"] = pred_df.groupby(by=labels).mean()[response]
    bin_df["PopulationMean"] = pop_mean
    # Compare the average value of response for the predictors in each bin
    msd = "MeanSquaredDiff"
    wmsd = "WeightedMeanSquaredDiff"
    bin_df[msd] = (bin_df["BinMean"] - bin_df["PopulationMean"]) ** 2
    bin_df[wmsd] = (
        bin_df["Weight"] * (bin_df["BinMean"] - bin_df["PopulationMean"]) ** 2
    )
    bin_df = bin_df.reset_index()
    return bin_df


def calc_diff_with_mean_table(
    df: pd.DataFrame,
    predictor: str,
    response: str,
    n: int = 10,
) -> pd.DataFrame:
    bin_df = None
    ptype = features.determine_predictor_type(df[predictor])
    if ptype == features.FeatureType.CONTINUOUS:
        return calc_diff_with_mean_table_cont(df, predictor, response, n)
    elif ptype == features.FeatureType.CATEGORICAL:
        return calc_diff_with_mean_table_cat(df, predictor, response)
    return bin_df


def calc_proportional_diff(
    df: pd.DataFrame,
    predictor: str,
    response: str,
) -> pd.DataFrame:
    target = df[response].unique()[0]
    # Get total proportion for this target
    pop_prop = df[df[response] == target].count() / df[response].count()
    # Get category counts and target counts
    prop_df = pd.DataFrame()
    prop_df["CategoryCounts"] = df.groupby(by=predictor)[response].count()
    prop_df[f"TargetCounts"] = (
        df[df[response] == target].groupby(by=predictor)[response].count()
    )
    prop_df["Proportion"] = prop_df["TargetCounts"] / prop_df["CategoryCounts"]
    prop_df["PopProp"] = pop_prop[0]
    prop_df["MeanDiff"] = prop_df["Proportion"] - prop_df["PopProp"]
    prop_df["MeanSquaredDiff"] = prop_df["MeanDiff"] ** 2
    prop_df["WeightedMeanSquaredDiff"] = (
        prop_df["Proportion"] * prop_df["MeanSquaredDiff"]
    )
    return prop_df


def main() -> int:
    df = data.mpg
    cont_df = calc_diff_with_mean_table(df, "weight", "mpg")
    cat_df = calc_diff_with_mean_table(df, "origin", "mpg")
    df = data.titanic
    bool_df = calc_proportional_diff(df, "pclass", "survived")
    print(cont_df, "\n", cat_df, "\n", bool_df)


if __name__ == "__main__":
    sys.exit(main())
