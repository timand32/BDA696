"""
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Figure
from plotly.subplots import make_subplots


def plot_violin(
    x: pd.Series,
    y: pd.Series,
    subtitle: str = None,
) -> Figure:
    df = x.to_frame().join(y)
    df = df.dropna()
    x = df[x.name]
    y = df[y.name]
    layout = {
        "title": f"{y.name} by {x.name}",
        "xaxis_title": f"{y.name}",
        "yaxis_title": f"{x.name}",
    }
    if subtitle:
        layout["title"] += f" ({subtitle})"
    figure = go.Figure(
        layout=layout,
    )
    for response in y.unique():
        figure.add_trace(
            go.Violin(
                x=y[y == response],
                y=x[y[y == response].index],
                name=f"{y.name}={response}",
                box_visible=True,
                meanline_visible=True,
                spanmode="hard",
            )
        )
    return figure


def save_figure(
    figure: Figure,
    filepath: str,
) -> None:
    path = Path(filepath)
    # Validate that the directory exists before saving
    path.parent.mkdir(parents=True, exist_ok=True)
    # lookup table for paths
    figure.write_html(path)


def plot_bins(x_name: str, y_name: str, bin_df: pd.DataFrame) -> Figure:
    figure = make_subplots(specs=[[{"secondary_y": True}]])
    figure.add_trace(
        go.Bar(
            x=(
                bin_df["lower_bin"].astype("float")
                + bin_df["upper_bin"].astype("float")
            )
            / 2,
            y=bin_df["bin_count"],
            width=(
                bin_df["upper_bin"].astype("float").max()
                - bin_df["lower_bin"].astype("float").max()
            ),
            opacity=0.5,
            yaxis="y2",
            name="population",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=(
                bin_df["lower_bin"].astype("float")
                + bin_df["upper_bin"].astype("float")
            )
            / 2,
            y=bin_df["bin_mean"],
            yaxis="y1",
            name="mean response",
        )
    )
    mean = bin_df["pop_mean"].mode()[0]
    figure.add_hline(y=mean)
    figure.update_layout(
        title_text="Binned difference with mean response vs bin",
    )
    figure.update_xaxes(title_text=f"{x_name} Bin")
    figure.update_yaxes(
        title_text=f"{y_name}",
        secondary_y=False,
        range=[0.0, 1.0],
    )
    figure.update_yaxes(
        title_text="Population",
        secondary_y=True,
        showgrid=False,
        zeroline=False,
    )
    return figure


if __name__ == "__main__":
    y = pd.Series([0, 0, 0, 1, 1, 1])
    x = pd.Series([1, 2, 3, 10, 20, 30])
    figure = plot_violin(x, y)
    figure.show()
    save_figure(figure, f"./output/plots/feature_{x.name}_plot.html")
