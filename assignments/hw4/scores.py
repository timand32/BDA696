"""Module for scoring predictors.
"""

import sys

import data
import features
import numpy as np
import pandas as pd
import statsmodels.api
from features import FeatureType
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler


def score_linear_regression(
    predictor: pd.Series,
    response: pd.Series,
) -> dict[str, object]:
    # The following is more or less adapted from the slides
    p = statsmodels.api.add_constant(predictor)
    lrm = statsmodels.api.OLS(response, p)
    lrm_fit = lrm.fit()
    t_value = round(lrm_fit.tvalues[1], 6)
    p_value = "{:.6e}".format(lrm_fit.pvalues[1])
    return {
        "linreg_t_value": t_value,
        "linreg_p_value": p_value,
    }


def score_logistic_regression(
    predictor: pd.Series,
    response: pd.Series,
) -> dict[str, object]:
    # The following is more or less adapted from the slides
    p = statsmodels.api.add_constant(predictor)
    lrm = statsmodels.api.Logit(response, p)
    lrm_fit = lrm.fit()
    t_value = round(lrm_fit.tvalues[1], 6)
    p_value = "{:.6e}".format(lrm_fit.pvalues[1])
    return {
        "logreg_t_value": t_value,
        "logreg_p_value": p_value,
    }


def score_single_predictor(
    predictor: pd.Series,
    response: pd.Series,
) -> dict[str, float]:
    scores_dict = dict()
    ptype = features.determine_predictor_type(predictor)
    rtype = features.determine_response_type(response)
    if ptype == FeatureType.CONTINUOUS:
        if rtype == FeatureType.CONTINUOUS:
            linr_dict = score_linear_regression(predictor, response)
            scores_dict = {**scores_dict, **linr_dict}
        if rtype == FeatureType.BOOLEAN:
            logr_dict = score_logistic_regression(predictor, response)
            scores_dict = {**scores_dict, **logr_dict}
    return scores_dict


def score_rfr_importances(
    df: pd.Series,
    predictors: list[str],
    response: str,
) -> np.ndarray:
    X = df[predictors]
    y = df[response]
    stdslr = StandardScaler()
    stdslr.fit(X)
    X = stdslr.transform(X)
    rfr = RandomForestRegressor()
    model = rfr.fit(X, y)
    return model.feature_importances_


def score_rfc_importances(
    df: pd.Series,
    predictors: list[str],
    response: str,
) -> np.ndarray:
    X = df[predictors]
    y = df[response]
    stdslr = StandardScaler()
    stdslr.fit(X)
    X = stdslr.transform(X)
    rfr = RandomForestClassifier()
    model = rfr.fit(X, y)
    return model.feature_importances_


def score_dataframe(
    df: pd.DataFrame,
    predictors: list[str],
    response: str,
) -> dict[str, dict[str, object]]:
    scores_dict = dict()
    rs = df[response]
    for predictor in predictors:
        ps = df[predictor]
        new_score_dict = score_single_predictor(ps, rs)
        scores_dict[predictor] = new_score_dict
    # Black wouldn't let me skip lines with \,
    # but flake8 instisted lines couln't be past 80...
    # So I shortened this only for here.
    CT = features.FeatureType.CONTINUOUS
    # Can only rff continuous, so filter for them.
    cont_preds = [
        p for p in predictors if features.determine_predictor_type(df[p]) == CT
    ]
    cont_df = df[list(cont_preds) + [response]]
    ptype = features.determine_response_type(df[response])
    if ptype is FeatureType.CONTINUOUS:
        rfr_importances = score_rfr_importances(cont_df, cont_preds, response)
        # Add importances in order they were generated
        for i, imp in enumerate(rfr_importances):
            scores_dict[cont_preds[i]]["rfr_importance"] = imp
    elif ptype is FeatureType.BOOLEAN:
        rfc_importances = score_rfc_importances(cont_df, cont_preds, response)
        for i, imp in enumerate(rfc_importances):
            scores_dict[cont_preds[i]]["rfc_importance"] = imp

    return scores_dict


def main() -> int:
    for df, predictors, response in data.test_cases:
        print(response)
        scores_dict = score_dataframe(df, predictors, response)
        print(scores_dict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
