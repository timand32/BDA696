"""Module for defining Plotter class and subclasses.
"""

from pathlib import Path

import pandas
import plotly.express as px

# import plotly.express as px
import plotly.graph_objects as go
from data import Dataset
from utility import (
    create_2D_cat_cont_diff_from_mean_table,
    create_2D_cat_diff_from_mean_table,
    create_2D_cont_diff_from_mean_table,
)


def save_plot(figure, title, path) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
    figure.write_html(path + title)
    return


def record_plot(df, type_, x_name, y_name, path) -> pandas.DataFrame:
    return df.append(
        {
            "type": type_,
            "x_name": x_name,
            "y_name": y_name,
            "path": path,
        },
        ignore_index=True,
    )


def plot_correlation_matrix(x, y, z, x_name, y_name) -> go.Figure:
    z_name = z.name
    title = f"{z_name} between {x_name} & {y_name}"
    annotations = []
    # Stack Overflow Q#60860121 helped here.
    for i, val in enumerate(z):
        font_color = ""
        if val > 0.0:
            font_color = "black"
        else:
            font_color = "white"
        annotations.append(
            {
                "x": x[i],
                "y": y[i],
                "font": {"color": font_color},
                "xref": "x1",
                "yref": "y1",
                "text": f"{str(round(val, 2))}",
                "showarrow": False,
            }
        )
    figure = go.Figure(
        data=go.Heatmap(
            x=x,
            y=y,
            z=z,
            text=z,
            zmin=-1.0,
            zmax=1.0,
            type="heatmap",
        ),
        layout={
            "title": title,
            "xaxis_title": x_name,
            "yaxis_title": y_name,
        },
    )
    return figure


def plot_dmr_matrix(x, y, z, populations, title, x_name, y_name) -> go.Figure:
    annotations = []
    # Stack Overflow Q#60860121 helped here.
    for i, val in enumerate(z):
        font_color = ""
        if val > 0.0:
            font_color = "black"
        else:
            font_color = "white"
        annotations.append(
            {
                "x": x[i],
                "y": y[i],
                "font": {"color": font_color},
                "xref": "x1",
                "yref": "y1",
                "text": f"{str(round(val, 2))} (pop: {populations[i]})",
                "showarrow": False,
            }
        )
    figure = go.Figure(
        data=go.Heatmap(
            x=x,
            y=y,
            z=z,
            # zmin= z.min(),
            zmid=0,
            # zmax = z.max(),
            type="heatmap",
        ),
        layout={
            "title": title,
            "xaxis_title": x_name,
            "yaxis_title": y_name,
            "annotations": annotations,
        },
    )
    return figure


class Plotter(object):
    """Base class for encapsulating plotting process."""

    def plot(
        self,
        dataset: Dataset,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        """Function should be overwritten
        to create and save appropriate plots
        and to return a dataframe of plot paths:
        """
        pass


class CategoricalXContinuousYPlotter:
    """"""

    def plot(
        self,
        dataset: Dataset,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        plot_df = pandas.DataFrame()
        X = dataset.categorical_X
        y = dataset.y
        df = pandas.DataFrame()
        df[y.name] = y
        for _, x in X.items():
            df[x.name] = x
            figure = px.violin(
                df,
                x=x.name,
                y=y.name,
                color=x.name,
                box=True,
                title=f"`{y.name}` (cont.) by `{x.name}` (bool.)",
            )
            dr = path + "plot/"
            title = f"{x.name}_{y.name}.html"
            save_plot(figure, title, dr)
            plot_df = record_plot(
                df=plot_df,
                type_="violin",
                x_name=x.name,
                y_name=y.name,
                path=f"../plot/{title}",
            )
        return plot_df


class ContinuousXContinuousYPlotter:
    """"""

    def plot(
        self,
        dataset: Dataset,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        plot_df = pandas.DataFrame()
        X = dataset.continuous_X
        y = dataset.y
        df = pandas.DataFrame()
        df[y.name] = y
        for _, x in X.items():
            df[x.name] = x
            figure = px.scatter(
                df,
                x=x.name,
                y=y.name,
                trendline="ols",
                title=f"`{y.name}` (cont.) by `{x.name}` (cont.)",
            )
            dr = path + "plot/"
            title = f"{x.name}_{y.name}.html"
            save_plot(figure, title, dr)
            plot_df = record_plot(
                df=plot_df,
                type_="scatter",
                x_name=x.name,
                y_name=y.name,
                path=f"../plot/{title}",
            )
        return plot_df


class CategoricalXBooleanYPlotter:
    """"""

    def plot(
        self,
        dataset: Dataset,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        plot_df = pandas.DataFrame()
        X = dataset.categorical_X
        y = dataset.y
        df = pandas.DataFrame()
        df[y.name] = y
        for _, x in X.items():
            df[x.name] = x
            figure = px.density_heatmap(
                df,
                x=x.name,
                y=y.name,
                title=f"`{x.name}` (cat.) by `{y.name}` (bool.)",
            )
            dr = path + "plot/"
            title = f"{x.name}_{y.name}.html"
            save_plot(figure, title, dr)
            plot_df = record_plot(
                df=plot_df,
                type_="heatmap",
                x_name=x.name,
                y_name=y.name,
                path=f"../plot/{title}",
            )
        return plot_df


class ContinuousXBooleanYPlotter:
    """"""

    def plot(
        self,
        dataset: Dataset,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        plot_df = pandas.DataFrame()
        X = dataset.continuous_X
        y = dataset.y
        df = pandas.DataFrame()
        df[y.name] = y
        for _, x in X.items():
            df[x.name] = x
            figure = px.violin(
                df,
                x=y.name,
                y=x.name,
                color=y.name,
                box=True,
                title=f"`{x.name}` (cont.) by `{y.name}` (bool.)",
            )
            dr = path + "plot/"
            title = f"{x.name}_{y.name}.html"
            save_plot(figure, title, dr)
            plot_df = record_plot(
                df=plot_df,
                type_="violin",
                x_name=x.name,
                y_name=y.name,
                path=f"../plot/{title}",
            )
        return plot_df


class CategoricalCategoricalCorrPlotter:
    """"""

    def plot(
        self,
        dataset: Dataset,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        plot_df = pandas.DataFrame()
        x = rank_df["x"]
        y = rank_df["y"]
        z = rank_df["cramerv_corr"]
        figure = plot_correlation_matrix(x, y, z, "cat", "cat")
        dr = path + "plot/"
        title = "cat_cat_corr_matrix.html"
        save_plot(figure, title, dr)
        plot_df = record_plot(
            df=plot_df,
            type_="corr_matrix",
            x_name=x.name,
            y_name=y.name,
            path=f"../plot/{title}",
        )
        return plot_df


class CategoricalContinuousCorrPlotter:
    """"""

    def plot(
        self,
        dataset: Dataset,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        plot_df = pandas.DataFrame()
        x = rank_df["x"]
        y = rank_df["y"]
        z = rank_df["corr_ratio"]
        figure = plot_correlation_matrix(x, y, z, "cat", "cont")
        dr = path + "plot/"
        title = "cat_cont_corr_matrix.html"
        save_plot(figure, title, dr)
        plot_df = record_plot(
            df=plot_df,
            type_="corr_matrix",
            x_name=x.name,
            y_name=y.name,
            path=f"../plot/{title}",
        )
        return plot_df


class ContinuousContinuousCorrPlotter:
    """"""

    def plot(
        self,
        dataset: Dataset,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        plot_df = pandas.DataFrame()
        x = rank_df["x"]
        y = rank_df["y"]
        z = rank_df["pearson_coef"]
        figure = plot_correlation_matrix(x, y, z, "cont", "cont")
        dr = path + "plot/"
        title = "cont_cont_corr_matrix.html"
        save_plot(figure, title, dr)
        plot_df = record_plot(
            df=plot_df,
            type_="corr_matrix",
            x_name=x.name,
            y_name=y.name,
            path=f"../plot/{title}",
        )
        return plot_df


class CategoricalCategoricalBFPlotter:
    """"""

    def plot(
        self,
        dataset: Dataset,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        plot_df = pandas.DataFrame()
        key = ("categorical", "categorical")
        for c in dataset.X_combinations[key]:
            X = dataset.get_combination_X(c)
            y = dataset.y
            diff_df = create_2D_cat_diff_from_mean_table(X=X, y=y)
            x = diff_df["i_category"]
            y = diff_df["j_category"]
            z = pandas.Series(diff_df["dmr"] * diff_df["bin_w"])
            title = f"{c[0]} & {c[1]} (weighted difference from mean response)"
            figure = plot_dmr_matrix(
                x,
                y,
                z,
                diff_df["bin_pop"],
                title,
                c[0],
                c[1],
            )
            dr = path + "plot/"
            title = f"{c[0]}_{c[1]}_dmr_matrix.html"
            save_plot(figure, title, dr)
            plot_df = record_plot(
                df=plot_df,
                type_="corr_matrix",
                x_name=c[0],
                y_name=c[1],
                path=f"../plot/{title}",
            )
        return plot_df


class CategoricalContinuousBFPlotter:
    """"""

    def plot(
        self,
        dataset: Dataset,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        plot_df = pandas.DataFrame()
        key = ("categorical", "continuous")
        for c in dataset.X_combinations[key]:
            X = dataset.get_combination_X(c)
            y = dataset.y
            diff_df = create_2D_cat_cont_diff_from_mean_table(X=X, y=y)
            x = diff_df["i_category"]
            y = [str(j) for j in diff_df["j_interval"].to_list()]
            z = pandas.Series(diff_df["dmr"] * diff_df["bin_w"])
            title = f"{c[0]} & {c[1]} (weighted difference from mean response)"
            figure = plot_dmr_matrix(
                x,
                y,
                z,
                diff_df["bin_pop"],
                title,
                c[0],
                c[1],
            )
            dr = path + "plot/"
            title = f"{c[0]}_{c[1]}_dmr_matrix.html"
            save_plot(figure, title, dr)
            plot_df = record_plot(
                df=plot_df,
                type_="corr_matrix",
                x_name=c[0],
                y_name=c[1],
                path=f"../plot/{title}",
            )
        return plot_df


class ContinuousContinuousBFPlotter:
    """"""

    def plot(
        self,
        dataset: Dataset,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        plot_df = pandas.DataFrame()
        key = ("continuous", "continuous")
        for c in dataset.X_combinations[key]:
            X = dataset.get_combination_X(c)
            y = dataset.y
            diff_df = create_2D_cont_diff_from_mean_table(X=X, y=y)
            x = [str(i) for i in diff_df["i_interval"].to_list()]
            y = [str(i) for i in diff_df["j_interval"].to_list()]
            z = pandas.Series(diff_df["dmr"] * diff_df["bin_w"])
            title = f"{c[0]} & {c[1]} (weighted difference from mean response)"
            figure = plot_dmr_matrix(
                x,
                y,
                z,
                diff_df["bin_pop"],
                title,
                c[0],
                c[1],
            )
            dr = path + "plot/"
            title = f"{c[0]}_{c[1]}_dmr_matrix.html"
            save_plot(figure, title, dr)
            plot_df = record_plot(
                df=plot_df,
                type_="corr_matrix",
                x_name=c[0],
                y_name=c[1],
                path=f"../plot/{title}",
            )
        return plot_df
