"""Module for defining Ranker class and subclasses.
"""

import pandas
from data import Dataset
from scipy.stats import pearsonr
from utility import (
    cat_cont_correlation_ratio,
    cat_correlation,
    create_2D_cat_cont_diff_from_mean_table,
    create_2D_cat_diff_from_mean_table,
    create_2D_cont_diff_from_mean_table,
)


class Ranker(object):
    """Base class for encapsulating ranking process."""

    def rank(self, dataset: Dataset) -> pandas.DataFrame:
        pass


class CategoricalXContinuousYRanker:
    """"""

    def rank(self, dataset: Dataset) -> pandas.DataFrame:
        rank_df = pandas.DataFrame()
        return rank_df


class ContinuousXContinuousYRanker:
    """"""

    def rank(self, dataset: Dataset) -> pandas.DataFrame:
        rank_df = pandas.DataFrame()
        return rank_df


class CategoricalXBooleanYRanker:
    """"""

    def rank(self, dataset: Dataset) -> pandas.DataFrame:
        rank_df = pandas.DataFrame()
        return rank_df


class ContinuousXBooleanYRanker:
    """"""

    def rank(self, dataset: Dataset) -> pandas.DataFrame:
        rank_df = pandas.DataFrame()
        return rank_df


class CategoricalCategoricalCorrRanker:
    """"""

    def rank(self, dataset: Dataset) -> pandas.DataFrame:
        """Point bi-serial correlation."""
        rank_df = pandas.DataFrame()
        key = ("categorical", "categorical")
        for combination in dataset.X_combinations[key]:
            x = dataset.X[combination[0]].values
            y = dataset.X[combination[1]].values
            cramerv_corr = cat_correlation(x=x, y=y)
            rank_df = rank_df.append(
                other={
                    "x": combination[0],
                    "y": combination[1],
                    "cramerv_corr": cramerv_corr,
                    "abs_corr": abs(cramerv_corr),
                },
                ignore_index=True,
            )
        rank_df = rank_df.sort_values(
            by="abs_corr",
            ascending=False,
        )
        rank_df["rank"] = range(0, len(rank_df["x"]))
        return rank_df


class CategoricalContinuousCorrRanker:
    """"""

    def rank(self, dataset: Dataset) -> pandas.DataFrame:
        rank_df = pandas.DataFrame()
        key = ("categorical", "continuous")
        for combination in dataset.X_combinations[key]:
            categories = dataset.X[combination[0]]
            values = dataset.X[combination[1]]
            corr_ratio = cat_cont_correlation_ratio(
                categories=categories, values=values
            )
            rank_df = rank_df.append(
                other={
                    "x": combination[0],
                    "y": combination[1],
                    "corr_ratio": corr_ratio,
                    "abs_ratio": abs(corr_ratio),
                },
                ignore_index=True,
            )
        rank_df = rank_df.sort_values(
            by="abs_ratio",
            ascending=False,
        )
        rank_df["rank"] = range(0, len(rank_df["x"]))
        return rank_df


class ContinuousContinuousCorrRanker:
    """"""

    def rank(self, dataset: Dataset) -> pandas.DataFrame:
        """Easy case: use Pearson Coefficient"""
        rank_df = pandas.DataFrame()
        key = ("continuous", "continuous")
        for combination in dataset.X_combinations[key]:
            x = dataset.X[combination[0]]
            y = dataset.X[combination[1]]
            pearson_coef, _ = pearsonr(x=x, y=y)
            rank_df = rank_df.append(
                other={
                    "x": combination[0],
                    "y": combination[1],
                    "pearson_coef": pearson_coef,
                    "abs_coef": abs(pearson_coef),
                },
                ignore_index=True,
            )
        rank_df = rank_df.sort_values(
            by="abs_coef",
            ascending=False,
        )
        rank_df["rank"] = range(0, len(rank_df["x"]))
        return rank_df


class CategoricalCategoricalBFRanker:
    """"""

    def rank(self, dataset: Dataset) -> pandas.DataFrame:
        rank_df = pandas.DataFrame()
        key = ("categorical", "categorical")
        for combination in dataset.X_combinations[key]:
            y = dataset.y
            X = dataset.get_combination_X(combination)
            diff_df = create_2D_cat_diff_from_mean_table(X, y)
            avg_dmrsq_unwgt = diff_df["dmrsq"].mean()
            avg_dmrsq_wgt = (diff_df["dmrsq"] * diff_df["bin_w"]).mean()
            rank_df = rank_df.append(
                other={
                    "x": combination[0],
                    "y": combination[1],
                    "avg_dmrsq_unwgt": avg_dmrsq_unwgt,
                    "avg_dmrsq_wgt": avg_dmrsq_wgt,
                },
                ignore_index=True,
            )
        rank_df = rank_df.sort_values(
            by="avg_dmrsq_wgt",
            ascending=False,
        )
        rank_df["rank"] = range(0, len(rank_df["x"]))
        return rank_df


class CategoricalContinuousBFRanker:
    """"""

    def rank(self, dataset: Dataset) -> pandas.DataFrame:
        rank_df = pandas.DataFrame()
        key = ("categorical", "continuous")
        for combination in dataset.X_combinations[key]:
            y = dataset.y
            X = dataset.get_combination_X(combination)
            diff_df = create_2D_cat_cont_diff_from_mean_table(X, y)
            avg_dmrsq_unwgt = diff_df["dmrsq"].mean()
            avg_dmrsq_wgt = (diff_df["dmrsq"] * diff_df["bin_w"]).mean()
            rank_df = rank_df.append(
                other={
                    "x": combination[0],
                    "y": combination[1],
                    "avg_dmrsq_unwgt": avg_dmrsq_unwgt,
                    "avg_dmrsq_wgt": avg_dmrsq_wgt,
                },
                ignore_index=True,
            )
        rank_df = rank_df.sort_values(
            by="avg_dmrsq_wgt",
            ascending=False,
        )
        rank_df["rank"] = range(0, len(rank_df["x"]))
        return rank_df


class ContinuousContinuousBFRanker:
    """"""

    def rank(self, dataset: Dataset) -> pandas.DataFrame:
        rank_df = pandas.DataFrame()
        key = ("continuous", "continuous")
        for combination in dataset.X_combinations[key]:
            y = dataset.y
            X = dataset.get_combination_X(combination)
            diff_df = create_2D_cont_diff_from_mean_table(X, y)
            avg_dmrsq_unwgt = diff_df["dmrsq"].mean()
            avg_dmrsq_wgt = (diff_df["dmrsq"] * diff_df["bin_w"]).mean()
            rank_df = rank_df.append(
                other={
                    "x": combination[0],
                    "y": combination[1],
                    "avg_dmrsq_unwgt": avg_dmrsq_unwgt,
                    "avg_dmrsq_wgt": avg_dmrsq_wgt,
                },
                ignore_index=True,
            )
        rank_df = rank_df.sort_values(
            by="avg_dmrsq_wgt",
            ascending=False,
        )
        rank_df["rank"] = range(0, len(rank_df["x"]))
        return rank_df
