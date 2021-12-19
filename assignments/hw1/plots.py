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
        subplot_titles=["Sepal Width vs. Length", "Petal Width vs. Length"],
    )
    sepal_plot = px.scatter(
        data_frame=iris_df,
        x="sepal_width",
        y="sepal_length",
        color="class",
    )
    petal_plot = px.scatter(
        data_frame=iris_df,
        x="petal_width",
        y="petal_length",
        color="class",
    )

    # Stack exchange question 60633891 really helped here.
    for trace in sepal_plot.data:
        figure.add_trace(trace, 1, 1)
    for trace in petal_plot.data:
        # As per my code buddy Amy's suggestion
        # Based on the way I did this, each trace needs this to be False
        trace.showlegend = False
        figure.add_trace(trace, 1, 2)

    # Stack exchange 58849925 helped here understanding editing Figures.
    figure.layout["xaxis"]["title"] = "sepal width (cm)"
    figure.layout["yaxis"]["title"] = "sepal length (cm)"
    figure.layout["xaxis2"]["title"] = "petal width (cm)"
    figure.layout["yaxis2"]["title"] = "petal length (cm)"
    figure.layout["title"] = "Scatterplots of Iris Features"

    return figure


_vsub_titles = ["Sepal Width", "Sepal Length", "Petal Width", "Petal Length"]


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
            x="petal_width",
            color="class",
        )
    )
    plots.append(
        px.violin(
            data_frame=iris_df,
            x="petal_length",
            color="class",
        )
    )
    # Stack exchange question 60633891 really helped here.
    coordinates = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for (i, plot) in enumerate(plots):
        coord = coordinates[i]
        for trace in plot.data:
            # Don't add legends if it's not first plot
            if i != 0:
                trace.showlegend = False
            figure.add_trace(trace, coord[0], coord[1])

    # Stack exchange 58849925 helped here understanding editing Figures.
    figure.layout["xaxis"]["title"] = "sepal width (cm)"
    figure.layout["xaxis2"]["title"] = "sepal length (cm)"
    figure.layout["xaxis3"]["title"] = "petal width (cm)"
    figure.layout["xaxis4"]["title"] = "petal length (cm)"
    figure.layout["title"] = "Violin Plots of Iris Features"

    return figure


_bsub_titles = ["Sepal Width", "Sepal Length", "Petal Width", "Petal Length"]


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
            y="petal_width",
            x="class",
            color="class",
        )
    )
    plots.append(
        px.box(
            data_frame=iris_df,
            y="petal_length",
            x="class",
            color="class",
        )
    )
    # Stack exchange question 60633891 really helped here.
    coordinates = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for (i, plot) in enumerate(plots):
        coord = coordinates[i]
        for trace in plot.data:
            # Don't add legends if it's not first plot
            if i != 0:
                trace.showlegend = False
            figure.add_trace(trace, coord[0], coord[1])

    # Stack exchange 58849925 helped here understanding editing Figures.
    figure.layout["yaxis"]["title"] = "sepal width (cm)"
    figure.layout["yaxis2"]["title"] = "sepal length (cm)"
    figure.layout["yaxis3"]["title"] = "petal width (cm)"
    figure.layout["yaxis4"]["title"] = "petal length (cm)"
    figure.layout["xaxis"]["title"] = "class"
    figure.layout["xaxis2"]["title"] = "class"
    figure.layout["xaxis3"]["title"] = "class"
    figure.layout["xaxis4"]["title"] = "class"
    figure.layout["title"] = "Box Plots of Iris Features"

    return figure


def _generate_histograms(iris_df: pd.DataFrame) -> go.Figure:
    figure = psp.make_subplots(
        rows=2,
        cols=2,
        subplot_titles=_bsub_titles,
    )
    plots = []
    plots.append(
        px.histogram(
            data_frame=iris_df,
            x="sepal_width",
            color="class",
        )
    )
    plots.append(
        px.histogram(
            data_frame=iris_df,
            x="sepal_length",
            color="class",
        )
    )
    plots.append(
        px.histogram(
            data_frame=iris_df,
            x="petal_width",
            color="class",
        )
    )
    plots.append(
        px.histogram(
            data_frame=iris_df,
            x="petal_length",
            color="class",
        )
    )
    # Stack exchange question 60633891 really helped here.
    coordinates = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for (i, plot) in enumerate(plots):
        coord = coordinates[i]
        for trace in plot.data:
            # Don't add legends if it's not first plot
            if i != 0:
                trace.showlegend = False
            figure.add_trace(trace, coord[0], coord[1])

    # Stack exchange 58849925 helped here understanding editing Figures.
    figure.layout["xaxis"]["title"] = "sepal width (cm)"
    figure.layout["xaxis2"]["title"] = "sepal length (cm)"
    figure.layout["xaxis3"]["title"] = "petal width (cm)"
    figure.layout["xaxis4"]["title"] = "petal length (cm)"
    figure.layout["yaxis"]["title"] = "frequency"
    figure.layout["yaxis2"]["title"] = "frequency"
    figure.layout["yaxis3"]["title"] = "frequency"
    figure.layout["yaxis4"]["title"] = "frequency"
    figure.layout["title"] = "Histogram Plots of Iris Features"

    return figure


def _generate_scatterplot_matrix(iris_df: pd.DataFrame):
    # Adapted from https://plotly.com/python/splom/.
    figure = px.scatter_matrix(
        iris_df,
        title="Scatterplot Matrix of Iris Features",
        dimensions=[
            "sepal_width",
            "sepal_length",
            "petal_width",
            "petal_length",
        ],
        color="class",
    )
    return figure


def generate_plots(iris_df: pd.DataFrame) -> list():
    plots = list()
    plots.append(_generate_scatterplot(iris_df=iris_df))
    plots.append(_generate_violinplots(iris_df=iris_df))
    plots.append(_generate_boxplots(iris_df=iris_df))
    plots.append(_generate_histograms(iris_df=iris_df))
    plots.append(_generate_scatterplot_matrix(iris_df))
    return plots


def main() -> int:
    iris_df = data.load_data()
    plots = generate_plots(iris_df=iris_df)
    for plot in plots:
        plot.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
