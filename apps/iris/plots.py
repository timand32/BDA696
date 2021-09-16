"""Module for generating plots of the Iris data set.
"""
import sys

import data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as psp


def _generate_scatterplot(iris_df: pd.DataFrame) -> go.Figure:
    figure = psp.make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Sepal Width vs. Length", "Pedal Width vs. Length"],
    )
    sepal_plot = px.scatter(
        data_frame=iris_df,
        x="sepal_width",
        y="sepal_length",
        color="class",
    )
    pedal_plot = px.scatter(
        data_frame=iris_df, x="pedal_width", y="pedal_length", color="class"
    )

    # Stack exchange question 60633891 really helped here.
    for trace in sepal_plot.data:
        figure.add_trace(trace, 1, 1)
    for trace in pedal_plot.data:
        figure.add_trace(trace, 1, 2)

    # Stack exchange 58849925 helped here understanding editing Figures.
    figure.layout["xaxis"]["title"] = "sepal width"
    figure.layout["yaxis"]["title"] = "sepal length"
    figure.layout["xaxis2"]["title"] = "pedal width"
    figure.layout["yaxis2"]["title"] = "pedal length"
    figure.layout["title"] = "Scatterplots of Iris Features"

    return figure


def generate_plots(iris_df: pd.DataFrame) -> list():
    plots = list()
    plots.append(_generate_scatterplot(iris_df=iris_df))
    return plots


def main() -> int:
    iris_df = data.load_data()
    plots = generate_plots(iris_df=iris_df)
    for plot in plots:
        plot.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
