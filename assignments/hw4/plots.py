"""Module for plotting response and predictor types.
"""

import sys
from pathlib import Path

import data
import features
import pandas as pd
import plotly.express as px
from features import FeatureType
from plotly.graph_objects import Figure


def plot_cat_predictor_with_bool_response(
    predictor: pd.Series, response: pd.Series
) -> list[Figure]:
    # Heatplot, as per lecture
    fig_list = list()
    pname = predictor.name
    rname = response.name
    df = pd.DataFrame({pname: predictor, rname: response})
    # Add each figure to return list
    fig_list.append(
        px.density_heatmap(
            df,
            x=pname,
            y=rname,
            title=f"`{pname}` (cat.) by `{rname}` (bool.)",
        ),
    )
    return fig_list


def plot_cont_predictor_with_bool_response(
    predictor: pd.Series, response: pd.Series
) -> list[Figure]:
    # Violin plot and dist plot, per lecture
    fig_list = list()
    pname = predictor.name
    rname = response.name
    df = pd.DataFrame({pname: predictor, rname: response})
    # Add each figure to return list
    fig_list.append(
        px.histogram(
            df,
            x=pname,
            color=rname,
            histnorm="probability",
            barmode="overlay",
            marginal="rug",
            title=f"`{pname}` (cont.) by `{rname}` (bool.)",
        )
    )
    fig_list.append(
        px.violin(
            df,
            x=rname,
            y=pname,
            color=rname,
            box=True,
            title=f"`{pname}` (cont.) by `{rname}` (bool.)",
        )
    )
    return fig_list


def plot_cat_predictor_with_cont_response(
    predictor: pd.Series, response: pd.Series
) -> list[Figure]:
    # Violin plot and dist plot, per lecture
    fig_list = list()
    pname = predictor.name
    rname = response.name
    df = pd.DataFrame({pname: predictor, rname: response})
    # Add each figure to return list
    fig_list.append(
        px.histogram(
            df,
            x=rname,
            color=pname,
            histnorm="probability",
            barmode="overlay",
            marginal="rug",
            title=f"`{rname}` (cont.) by `{pname}` (cat.)",
        )
    )
    fig_list.append(
        px.violin(
            df,
            x=pname,
            y=rname,
            color=pname,
            box=True,
            title=f"`{rname}` (cont.) by `{pname}` (cat.)",
        )
    )
    return fig_list


def plot_cont_predictor_with_cont_response(
    predictor: pd.Series, response: pd.Series
) -> list[Figure]:
    # Scatterplot and trendline, per lecture
    fig_list = list()
    pname = predictor.name
    rname = response.name
    df = pd.DataFrame({pname: predictor, rname: response})
    # Add each figure to return list
    fig_list.append(
        px.scatter(
            df,
            x=pname,
            y=rname,
            trendline="ols",
            title=f"`{rname}` (cont.) by `{pname}` (cont.)",
        )
    )
    return fig_list


def plot_predictor(predictor: pd.Series, response: pd.Series) -> list[Figure]:
    ptype = features.determine_predictor_type(predictor)
    rtype = features.determine_response_type(response)
    if rtype == FeatureType.BOOLEAN:
        if ptype == FeatureType.CATEGORICAL:
            return plot_cat_predictor_with_bool_response(predictor, response)
        elif ptype == FeatureType.CONTINUOUS:
            return plot_cont_predictor_with_bool_response(predictor, response)
    elif rtype == FeatureType.CONTINUOUS:
        if ptype == FeatureType.CATEGORICAL:
            return plot_cat_predictor_with_cont_response(predictor, response)
        elif ptype == FeatureType.CONTINUOUS:
            return plot_cont_predictor_with_cont_response(predictor, response)
    else:
        raise ValueError(
            f"Unexpected feature types:\n\
            (predictor:{ptype}, response:{rtype})"
        )


def plot_scores(
    df: pd.DataFrame,
    scores: dict[tuple[str:float]],
    response: str,
    predictors: list[str] = None,
) -> dict[list[Figure]]:
    fig_dict = dict()
    # Default to everything if predictors is None
    if predictors is None:
        predictors = df.columns
        predictors = predictors.drop(response)
    return fig_dict


def plot_dataset(
    df: pd.DataFrame,
    scores: dict[str, dict[str, object]],
    response: str,
    predictors: list[str] = None,
) -> dict[list[Figure]]:
    fig_dict = dict()
    # Default to everything if predictors is None
    if predictors is None:
        predictors = df.columns
        predictors = predictors.drop(response)
    for p in predictors:
        fig_dict[p] = plot_predictor(df[p], df[response])
    scores_fig_dict = plot_scores(df, scores, response, predictors)
    fig_dict = {**fig_dict, **scores_fig_dict}
    return fig_dict


def save_plots(
    fig_dict: dict[list[Figure]],
    path: str = "./output/plots/",
) -> None:
    # Make output directory if it doesn't exist
    Path(path).mkdir(parents=True, exist_ok=True)
    for key, fig_list in fig_dict.items():
        for i, fig in enumerate(fig_list):
            fig.write_html(path + f"{key}_{i}.html")


def main() -> int:
    scores = None
    for df, _, response in data.test_cases:
        fig_dict = plot_dataset(df, scores, response)
        save_plots(fig_dict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
