"""Module for plotting response and predictor types.
"""

import sys
from pathlib import Path

import data
import diffs
import features
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from features import FeatureType
from plotly.graph_objects import Figure


def plot_diff_with_mean(
    df: pd.DataFrame,
    predictor: str,
    response: str,
) -> dict[Figure]:
    fig_dict = dict()
    rtype = features.determine_response_type(df[response])
    if rtype == features.FeatureType.CONTINUOUS:
        d = diffs.calc_diff_with_mean_table(df, predictor, response)
        x = None
        if "BinCenter" in d.columns:
            x = d["BinCenter"]
        elif "Category" in d.columns:
            x = d["Category"]
        fig = go.Figure(
            data=[
                go.Bar(
                    x=x,
                    y=d["BinMean"],
                )
            ],
            layout=go.Layout(
                title=go.layout.Title(
                    text="Binned Difference with Mean of Response vs Bin"
                ),
            ),
        )
        fig.add_hline(y=d["PopulationMean"][0])
        fig_dict["diff"] = fig
    elif rtype == features.FeatureType.BOOLEAN:
        d = diffs.calc_proportional_diff(df, predictor, response)
        x = d.reset_index()[predictor]
        fig = go.Figure(
            data=[
                go.Bar(
                    x=x,
                    y=d["Proportion"],
                )
            ],
            layout=go.Layout(
                title=go.layout.Title(
                    text="Binned Difference with Prop. of Response vs Bin"
                ),
            ),
        )
        fig.add_hline(y=d["PopProp"].iloc[0])
        fig_dict["diff"] = fig
    return fig_dict


def plot_cat_predictor_with_bool_response(
    predictor: pd.Series, response: pd.Series
) -> dict[Figure]:
    # Heatplot, as per lecture
    fig_dict = dict()
    pname = predictor.name
    rname = response.name
    df = pd.DataFrame({pname: predictor, rname: response})
    # Add each figure to return list
    fig_dict["heatmap"] = px.density_heatmap(
        df,
        x=pname,
        y=rname,
        title=f"`{pname}` (cat.) by `{rname}` (bool.)",
    )
    return fig_dict


def plot_cont_predictor_with_bool_response(
    predictor: pd.Series, response: pd.Series
) -> dict[Figure]:
    # Violin plot and dist plot, per lecture
    fig_dict = dict()
    pname = predictor.name
    rname = response.name
    df = pd.DataFrame({pname: predictor, rname: response})
    # Add each figure to return dict
    fig_dict["histogram"] = px.histogram(
        df,
        x=pname,
        color=rname,
        histnorm="probability",
        barmode="overlay",
        marginal="rug",
        title=f"`{pname}` (cont.) by `{rname}` (bool.)",
    )
    fig_dict["violin"] = px.violin(
        df,
        x=rname,
        y=pname,
        color=rname,
        box=True,
        title=f"`{pname}` (cont.) by `{rname}` (bool.)",
    )
    return fig_dict


def plot_cat_predictor_with_cont_response(
    predictor: pd.Series, response: pd.Series
) -> dict[Figure]:
    # Violin plot and dist plot, per lecture
    fig_dict = dict()
    pname = predictor.name
    rname = response.name
    df = pd.DataFrame({pname: predictor, rname: response})
    # Add each figure to return list
    fig_dict["histogram"] = px.histogram(
        df,
        x=rname,
        color=pname,
        histnorm="probability",
        barmode="overlay",
        marginal="rug",
        title=f"`{rname}` (cont.) by `{pname}` (cat.)",
    )
    fig_dict["violin"] = px.violin(
        df,
        x=pname,
        y=rname,
        color=pname,
        box=True,
        title=f"`{rname}` (cont.) by `{pname}` (cat.)",
    )
    return fig_dict


def plot_cont_predictor_with_cont_response(
    predictor: pd.Series, response: pd.Series
) -> dict[str, Figure]:
    # Scatterplot and trendline, per lecture
    fig_dict = dict()
    pname = predictor.name
    rname = response.name
    df = pd.DataFrame({pname: predictor, rname: response})
    # Add each figure to return list
    fig_dict["scatter"] = px.scatter(
        df,
        x=pname,
        y=rname,
        trendline="ols",
        title=f"`{rname}` (cont.) by `{pname}` (cont.)",
    )
    return fig_dict


def plot_predictor(
    predictor: pd.Series,
    response: pd.Series,
) -> dict[Figure]:
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


def plot_dataset(
    df: pd.DataFrame,
    response: str,
    predictors: list[str] = None,
) -> dict[dict[str, Figure]]:
    fig_dict = dict()
    # Default to everything if predictors is None
    if predictors is None:
        predictors = df.columns
        predictors = predictors.drop(response)
    for p in predictors:
        fig_dict[p] = plot_predictor(df[p], df[response])
        fig_dict[p] = {**fig_dict[p], **plot_diff_with_mean(df, p, response)}
    # scores_fig_dict = plot_scores(df, scores, response, predictors)
    # fig_dict = {**fig_dict, **scores_fig_dict}
    return fig_dict


def save_plots(
    fig_dict: dict[dict[str, Figure]],
    path: str = "./output/plots/",
) -> None:
    # Make output directory if it doesn't exist
    Path(path).mkdir(parents=True, exist_ok=True)
    for pred_key, fd in fig_dict.items():
        for plot_key, fig in fd.items():
            file_path = f"{path}{pred_key}/"
            Path(file_path).mkdir(parents=True, exist_ok=True)
            fig.write_html(f"{file_path}{plot_key}.html")


def main() -> int:
    for df, _, response in data.test_cases:
        fig_dict = plot_dataset(df, response)
        save_plots(fig_dict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
