"""Module for defining Reporter class and subclasses.
"""

from pathlib import Path

import pandas
from data import Dataset


def style_table(styler):
    # Stack Overflow Q#64812819
    # Styler doesn't come with lines, had to add them.
    styler = styler.set_table_styles(
        [
            {"selector": "", "props": [("border", "1px solid grey")]},
            {"selector": "tbody td", "props": [("border", "1px solid grey")]},
            {"selector": "th", "props": [("border", "1px solid grey")]},
        ]
    )
    return styler


def save_table(styler, title, path) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
    file_path = path + title
    styler = style_table(styler)
    with open(file_path, "w+") as file:
        file.write(styler.render())
    return None


def add_links(rank_df, plot_col, response_name):
    p_link = (
        '<a target="_blank" href="../../predictors/plot/{0}_'
        + response_name
        + '.html">{0}</a>'
    )
    link = '<a target="_blank" href="{0}">LINK</a>'
    styler = rank_df.style.format(
        {
            "x": p_link,
            "y": p_link,
            plot_col: link,
        },
        escape="html",
        na_rep="NA",
    )
    return styler


class Reporter(object):
    """Base class for encapsulating plotting process."""

    def report(
        self,
        dataset: Dataset,
        plot_df: pandas.DataFrame,
        rank_df: pandas.DataFrame,
    ) -> pandas.DataFrame:
        pass


class CategoricalXContinuousYReporter:
    """"""

    def report(
        self,
        dataset: Dataset,
        plot_df: pandas.DataFrame,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        report_df = pandas.DataFrame()
        return report_df


class ContinuousXContinuousYReporter:
    """"""

    def report(
        self,
        dataset: Dataset,
        plot_df: pandas.DataFrame,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        report_df = pandas.DataFrame()
        return report_df


class CategoricalXBooleanYReporter:
    """"""

    def report(
        self,
        dataset: Dataset,
        plot_df: pandas.DataFrame,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        report_df = pandas.DataFrame()
        return report_df


class ContinuousXBooleanYReporter:
    """"""

    def report(
        self,
        dataset: Dataset,
        plot_df: pandas.DataFrame,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        report_df = pandas.DataFrame()
        return report_df


class CategoricalCategoricalCorrReporter:
    """"""

    def report(
        self,
        dataset: Dataset,
        plot_df: pandas.DataFrame,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        report_df = pandas.DataFrame()
        rank_df["corr_matrix"] = plot_df["path"][0]
        styler = add_links(rank_df, "corr_matrix", dataset.y.name)
        title = "cat_cat_corr_report.html"
        save_table(styler, title, path + "reports/")
        return report_df


class CategoricalContinuousCorrReporter:
    """"""

    def report(
        self,
        dataset: Dataset,
        plot_df: pandas.DataFrame,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        report_df = pandas.DataFrame()
        rank_df["corr_matrix"] = plot_df["path"][0]
        styler = add_links(rank_df, "corr_matrix", dataset.y.name)
        title = "cat_cont_corr_report.html"
        save_table(styler, title, path + "reports/")
        return report_df


class ContinuousContinuousCorrReporter:
    """"""

    def report(
        self,
        dataset: Dataset,
        plot_df: pandas.DataFrame,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        report_df = pandas.DataFrame()
        rank_df["corr_matrix"] = plot_df["path"][0]
        styler = add_links(rank_df, "corr_matrix", dataset.y.name)
        title = "cont_cont_corr_report.html"
        save_table(styler, title, path + "reports/")
        return report_df


class CategoricalCategoricalBFReporter:
    """"""

    def report(
        self,
        dataset: Dataset,
        plot_df: pandas.DataFrame,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        report_df = pandas.DataFrame()
        rank_df["dmr_matrix"] = plot_df["path"]
        styler = add_links(rank_df, "dmr_matrix", dataset.y.name)
        title = "cat_cat_bf_report.html"
        save_table(styler, title, path + "reports/")
        return report_df


class CategoricalContinuousBFReporter:
    """"""

    def report(
        self,
        dataset: Dataset,
        plot_df: pandas.DataFrame,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        report_df = pandas.DataFrame()
        report_df = pandas.DataFrame()
        rank_df["dmr_matrix"] = plot_df["path"]
        styler = add_links(rank_df, "dmr_matrix", dataset.y.name)
        title = "cat_cont_bf_report.html"
        save_table(styler, title, path + "reports/")
        return report_df


class ContinuousContinuousBFReporter:
    """"""

    def report(
        self,
        dataset: Dataset,
        plot_df: pandas.DataFrame,
        rank_df: pandas.DataFrame,
        path: str,
    ) -> pandas.DataFrame:
        report_df = pandas.DataFrame()
        report_df = pandas.DataFrame()
        rank_df["dmr_matrix"] = plot_df["path"]
        styler = add_links(rank_df, "dmr_matrix", dataset.y.name)
        title = "cont_cont_bf_report.html"
        save_table(styler, title, path + "reports/")
        return report_df
