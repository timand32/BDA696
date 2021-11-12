"""
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Figure


def plot_violin(
    x: pd.Series,
    y: pd.Series,
    subtitle: str = None,
) -> Figure:
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
):
    path = Path(filepath)
    # Validate that the directory exists before saving
    path.parent.mkdir(parents=True, exist_ok=True)
    # lookup table for paths
    figure.write_html(path)


if __name__ == "__main__":
    y = pd.Series([0, 0, 0, 1, 1, 1])
    x = pd.Series([1, 2, 3, 10, 20, 30])
    figure = plot_violin(x, y)
    figure.show()
    save_figure(figure, f"./output/plots/feature_{x.name}_plot.html")
