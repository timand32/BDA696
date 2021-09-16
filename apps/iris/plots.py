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
    figure.layout["xaxis"]["title"] = "sepal width (cm)"
    figure.layout["yaxis"]["title"] = "sepal length (cm)"
    figure.layout["xaxis2"]["title"] = "pedal width (cm)"
    figure.layout["yaxis2"]["title"] = "pedal length (cm)"
    figure.layout["title"] = "Scatterplots of Iris Features"

    return figure


_vsub_titles = ["Sepal Width", "Sepal Length", "Pedal Width", "Pedal Length"]


def _generate_violinplots(iris_df: pd.DataFrame) -> go.Figure:
    figure = psp.make_subplots(
        rows=2,
        cols=2,
        subplot_titles=_vsub_titles,
    )
    plots = []
    plots.append(
        px.violin(
            data_frame=iris_df,
            x="sepal_width",
            color="class",
        )
    )
    plots.append(
        px.violin(
            data_frame=iris_df,
            x="sepal_length",
            color="class",
        )
    )
    plots.append(
        px.violin(
            data_frame=iris_df,
            x="pedal_width",
            color="class",
        )
    )
    plots.append(
        px.violin(
            data_frame=iris_df,
            x="pedal_length",
            color="class",
        )
    )
    print(plots)
    # Stack exchange question 60633891 really helped here.
    coordinates = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for (i, plot) in enumerate(plots):
        coord = coordinates[i]
        for trace in plot.data:
            figure.add_trace(trace, coord[0], coord[1])

    # Stack exchange 58849925 helped here understanding editing Figures.
    figure.layout["yaxis"]["title"] = "sepal width"
    figure.layout["yaxis2"]["title"] = "sepal length"
    figure.layout["yaxis3"]["title"] = "pedal width"
    figure.layout["yaxis4"]["title"] = "pedal length"
    figure.layout["title"] = "Violin Plots of Iris Features"

    return figure


_bsub_titles = ["Sepal Width", "Sepal Length", "Pedal Width", "Pedal Length"]


def _generate_boxplots(iris_df: pd.DataFrame) -> go.Figure:
    figure = psp.make_subplots(
        rows=2,
        cols=2,
        subplot_titles=_bsub_titles,
    )
    plots = []
    plots.append(
        px.box(
            data_frame=iris_df,
            y="sepal_width",
            x="class",
            color="class",
        )
    )
    plots.append(
        px.box(
            data_frame=iris_df,
            y="sepal_length",
            x="class",
            color="class",
        )
    )
    plots.append(
        px.box(
            data_frame=iris_df,
            y="pedal_width",
            x="class",
            color="class",
        )
    )
    plots.append(
        px.box(
            data_frame=iris_df,
            y="pedal_length",
            x="class",
            color="class",
        )
    )
    print(plots)
    # Stack exchange question 60633891 really helped here.
    coordinates = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for (i, plot) in enumerate(plots):
        coord = coordinates[i]
        for trace in plot.data:
            figure.add_trace(trace, coord[0], coord[1])

    # Stack exchange 58849925 helped here understanding editing Figures.
    figure.layout["yaxis"]["title"] = "sepal width (cm)"
    figure.layout["yaxis2"]["title"] = "sepal length (cm)"
    figure.layout["yaxis3"]["title"] = "pedal width (cm)"
    figure.layout["yaxis4"]["title"] = "pedal length (cm)"
    figure.layout["xaxis"]["title"] = "class"
    figure.layout["xaxis2"]["title"] = "class"
    figure.layout["xaxis3"]["title"] = "class"
    figure.layout["xaxis4"]["title"] = "class"
    figure.layout["title"] = "Box Plots of Iris Features"

    return figure


def generate_plots(iris_df: pd.DataFrame) -> list():
    plots = list()
    plots.append(_generate_scatterplot(iris_df=iris_df))
    plots.append(_generate_violinplots(iris_df=iris_df))
    plots.append(_generate_boxplots(iris_df=iris_df))
    return plots


def main() -> int:
    iris_df = data.load_data()
    plots = generate_plots(iris_df=iris_df)
    for plot in plots:
        plot.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
