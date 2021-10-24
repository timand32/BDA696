"""
"""

import numpy as np
import pandas as pd
import statsmodels.api
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler


def _calculate_linear_regression(
    predictor: pd.Series,
    response: pd.Series,
) -> pd.DataFrame:
    """"""
    p = statsmodels.api.add_constant(predictor)
    lrm = statsmodels.api.OLS(response, p)
    lrm_fit = lrm.fit()
    t_value = round(lrm_fit.tvalues[1], 6)
    p_value = "{:.6e}".format(lrm_fit.pvalues[1])
    return (t_value, p_value)


def _calculate_rfr_importance(
    df: pd.DataFrame,
    response: str,
) -> pd.DataFrame:
    """"""
    predictors = [f for f in df.columns if f is not response]
    X = df[predictors]
    y = df[response]
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    rfr = RandomForestRegressor()
    model = rfr.fit(X, y)
    importances = model.feature_importances_
    rfr_df = pd.DataFrame({"feature": predictors})
    rfr_df["metric_type"] = "rfr_importance"
    rfr_df["value"] = importances
    return rfr_df


def _calculate_msd(
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
    intervals = pd.qcut(ps, n, duplicates="drop")
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


def _score_features(
    metric_df: pd.DataFrame,
) -> pd.DataFrame:
    """"""
    # Use the following metrics to score
    used_metrics = [
        "linreg_t_value",
        "rfr_importance",
        "weighted_mean_sq_diff_avg",
    ]
    score_df = pd.DataFrame()
    metric_df["max_value"] = 0
    metric_df["scaled_value"] = 0
    for m in used_metrics:
        metric_df.loc[metric_df["metric_type"] == m, "value"] = metric_df.loc[
            metric_df["metric_type"] == m,
            "value",
        ].abs()
        mt = "metric_type"  # I couldn't get black to stop formatting over 80
        metric_df.loc[metric_df[mt] == m, "max_value"] = metric_df.loc[
            metric_df["metric_type"] == m,
            "value",
        ].max()
        metric_df.loc[metric_df["metric_type"] == m, "scaled_value"] = (
            metric_df.loc[metric_df["metric_type"] == m, "value"]
            / metric_df.loc[metric_df["metric_type"] == m, "max_value"]
        )
    for f in metric_df["feature"].unique():
        value_loc = metric_df.loc[metric_df["feature"] == f, ["scaled_value"]]
        # Stack Overflow Q 1401712, essentially taking distance from (0,0,0)
        norm = np.linalg.norm(value_loc)
        score_df = score_df.append(
            {
                "feature": f,
                "metric_type": "score",
                "value": norm,
            },
            ignore_index=True,
        )
    return score_df


def calculate_cont_pred_cont_resp_metrics(
    df: pd.DataFrame,
    response: str,
) -> pd.DataFrame:
    """"""
    # Iterate and calculate linear regressions
    metric_df = pd.DataFrame()
    r_series = df[response]
    predictors = [f for f in df.columns if f is not response]
    for p in predictors:
        p_series = df[p]
        t_value, p_value = _calculate_linear_regression(p_series, r_series)
        metric_df = metric_df.append(
            {"feature": p, "metric_type": "linreg_t_value", "value": t_value},
            ignore_index=True,
        )
        metric_df = metric_df.append(
            {
                "feature": p,
                "metric_type": "linreg_p_value",
                "value": float(p_value),
            },
            ignore_index=True,
        )
        msd_df = _calculate_msd(df, p, response)
        metric_df = metric_df.append(
            {
                "feature": p,
                "metric_type": "mean_sq_diff_avg",
                "value": msd_df["MeanSquaredDiff"].mean(),
            },
            ignore_index=True,
        )
        metric_df = metric_df.append(
            {
                "feature": p,
                "metric_type": "weighted_mean_sq_diff_avg",
                "value": msd_df["WeightedMeanSquaredDiff"].mean(),
            },
            ignore_index=True,
        )
    metric_df = metric_df.append(
        _calculate_rfr_importance(df, response), ignore_index=True
    )
    metric_df = metric_df.append(
        _score_features(
            metric_df[
                metric_df["metric_type"] != "diff_mean_sq_avg",
            ]
        ),
        ignore_index=True,
    )
    return metric_df
