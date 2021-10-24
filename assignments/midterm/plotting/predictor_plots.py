"""
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _plot_cat_pred_bool_resp(
    predictor: pd.Series,
    response: pd.Series,
) -> go.Figure:
    """Plot a plotly figure of a categorical predictor
    with a boolean response.

    Plot includes heatmap of predictor by response.
    """
    df = pd.DataFrame({predictor.name: predictor, response.name: response})
    figure = px.density_heatmap(
        df,
        x=predictor.name,
        y=response.name,
        title=f"`{predictor.name}` (cat.) by `{response.name}` (bool.)",
    )
    figure.update_yaxes(tick0=0, dtick=1)
    return figure


def _plot_cont_pred_bool_resp(
    predictor: pd.Series,
    response: pd.Series,
) -> go.Figure:
    """Plot a plotly figure of a continuous predictor
    with a boolean response.

    Plot includes a histogram and a violin plot of predictor by response.
    """
    df = pd.DataFrame({predictor.name: predictor, response.name: response})
    figure = px.violin(
        df,
        x=response.name,
        y=predictor.name,
        color=predictor.name,
        box=True,
        title=f"`{predictor.name}` (cont.) by `{response.name}` (bool.)",
    )
    return figure


def _plot_cat_pred_cont_resp(
    predictor: pd.Series,
    response: pd.Series,
) -> go.Figure:
    """Plot a plotly figure of a categorical predictor
    with a continuous response.

    Plot includes a histogram and a violin plot of predictor by response.
    """
    df = pd.DataFrame({predictor.name: predictor, response.name: response})
    figure = px.violin(
        df,
        x=predictor.name,
        y=response.name,
        color=predictor.name,
        box=True,
        title=f"`{response.name}` (cont.) by `{predictor.name}` (bool.)",
    )
    return figure


def _plot_cont_pred_cont_resp(
    predictor: pd.Series,
    response: pd.Series,
) -> go.Figure:
    """Plot a plotly figure of a categorical predictor
    with a continuous response.

    Plots a scatterplot.
    """
    df = pd.DataFrame({predictor.name: predictor, response.name: response})
    figure = px.scatter(
        df,
        x=predictor.name,
        y=response.name,
        trendline="ols",
        title=f"`{response.name}` (cont.) by `{predictor.name}` (cont.)",
    )
    return figure


def _plot_predictor(
    predictor: pd.Series,
    predictor_type: str,
    response: pd.Series,
    response_type: str,
) -> go.Figure:
    """Determine correct predictor plot, then plot predictor."""
    if response_type == "continuous":
        if predictor_type == "categorical":
            figure = _plot_cat_pred_cont_resp(predictor, response)
        elif predictor_type == "continuous":
            figure = _plot_cont_pred_cont_resp(predictor, response)
        else:
            raise ValueError(f"Unsupported predictor type {predictor_type}")
    elif response_type == "boolean":
        if predictor_type == "categorical":
            figure = _plot_cat_pred_bool_resp(predictor, response)
        elif predictor_type == "continuous":
            figure = _plot_cont_pred_bool_resp(predictor, response)
        else:
            raise ValueError(f"Unsupported predictor type {predictor_type}")
    else:
        raise ValueError(f"Unsupported predictor type {response_type}")
    return figure


def plot_predictors(
    data_df: pd.DataFrame,
    feature_df: pd.DataFrame,
    save_dir: str,
) -> pd.DataFrame:
    fig_df = pd.DataFrame()
    response_loc = feature_df.loc[
        feature_df["is_response"],
        ["feature", "feature_type"],
    ]
    response_name = response_loc.loc[:, "feature"].iloc[0]
    response_type = response_loc.loc[:, "feature_type"].iloc[0]
    response = data_df[response_name]
    predictor_loc = feature_df.loc[
        ~feature_df["is_response"],
        ["feature", "feature_type"],
    ]
    for row in predictor_loc.itertuples():
        predictor_name = row.feature
        predictor_type = row.feature_type
        predictor = data_df[predictor_name]
        figure = _plot_predictor(
            predictor=predictor,
            predictor_type=predictor_type,
            response=response,
            response_type=response_type,
        )
        full_dir = save_dir + f"plots/predictors/"

        Path(full_dir).mkdir(parents=True, exist_ok=True)
        save_path = full_dir + f"{predictor_name}.html"
        figure.write_html(save_path)
        fig_df = fig_df.append(
            {
                "plot_type": "predictor",
                "plot_subject": predictor_name,
                "plot_path": save_path,
            },
            ignore_index=True,
        )
    return fig_df
