"""
"""
from pathlib import Path
from typing import Dict

from analysis import Analysis
from data import Dataset
from plotter import (
    CategoricalCategoricalBFPlotter,
    CategoricalCategoricalCorrPlotter,
    CategoricalContinuousBFPlotter,
    CategoricalContinuousCorrPlotter,
    CategoricalXBooleanYPlotter,
    CategoricalXContinuousYPlotter,
    ContinuousContinuousBFPlotter,
    ContinuousContinuousCorrPlotter,
    ContinuousXBooleanYPlotter,
    ContinuousXContinuousYPlotter,
)
from ranker import (
    CategoricalCategoricalBFRanker,
    CategoricalCategoricalCorrRanker,
    CategoricalContinuousBFRanker,
    CategoricalContinuousCorrRanker,
    CategoricalXBooleanYRanker,
    CategoricalXContinuousYRanker,
    ContinuousContinuousBFRanker,
    ContinuousContinuousCorrRanker,
    ContinuousXBooleanYRanker,
    ContinuousXContinuousYRanker,
)
from reporter import (
    CategoricalCategoricalBFReporter,
    CategoricalCategoricalCorrReporter,
    CategoricalContinuousBFReporter,
    CategoricalContinuousCorrReporter,
    CategoricalXBooleanYReporter,
    CategoricalXContinuousYReporter,
    ContinuousContinuousBFReporter,
    ContinuousContinuousCorrReporter,
    ContinuousXBooleanYReporter,
    ContinuousXContinuousYReporter,
)


class Analyzer(object):
    """Class for generating Analysis objects based on a given dataset."""

    def __init__(self, dataset: Dataset, path: str):
        self.dataset: Dataset = dataset
        self.path = path + f"{dataset.title}/"
        Path(path).mkdir(parents=True, exist_ok=True)

    def analyze_predictors(self) -> Dict[str, Analysis]:
        return self.__handle_response()

    def analyze_correlations(self) -> Dict[str, Analysis]:
        analyses = dict()
        key = ("categorical", "categorical")
        if self.dataset.X_combinations[key]:
            analyses[key] = Analysis(
                dataset=self.dataset,
                plotter=CategoricalCategoricalCorrPlotter(),
                ranker=CategoricalCategoricalCorrRanker(),
                reporter=CategoricalCategoricalCorrReporter(),
                path=self.path + "correlations/",
            )
        key = ("categorical", "continuous")
        if self.dataset.X_combinations[key]:
            analyses[key] = Analysis(
                dataset=self.dataset,
                plotter=CategoricalContinuousCorrPlotter(),
                ranker=CategoricalContinuousCorrRanker(),
                reporter=CategoricalContinuousCorrReporter(),
                path=self.path + "correlations/",
            )
        key = ("continuous", "continuous")
        if self.dataset.X_combinations[key]:
            analyses[key] = Analysis(
                dataset=self.dataset,
                plotter=ContinuousContinuousCorrPlotter(),
                ranker=ContinuousContinuousCorrRanker(),
                reporter=ContinuousContinuousCorrReporter(),
                path=self.path + "correlations/",
            )
        return analyses

    def analyze_brute_force(self) -> Dict[str, Analysis]:
        analyses = dict()
        key = ("categorical", "categorical")
        if self.dataset.X_combinations[key]:
            analyses[key] = Analysis(
                dataset=self.dataset,
                plotter=CategoricalCategoricalBFPlotter(),
                ranker=CategoricalCategoricalBFRanker(),
                reporter=CategoricalCategoricalBFReporter(),
                path=self.path + "bruteforce/",
            )
        key = ("categorical", "continuous")
        if self.dataset.X_combinations[key]:
            analyses[key] = Analysis(
                dataset=self.dataset,
                plotter=CategoricalContinuousBFPlotter(),
                ranker=CategoricalContinuousBFRanker(),
                reporter=CategoricalContinuousBFReporter(),
                path=self.path + "bruteforce/",
            )
        key = ("continuous", "continuous")
        if self.dataset.X_combinations[key]:
            analyses[key] = Analysis(
                dataset=self.dataset,
                plotter=ContinuousContinuousBFPlotter(),
                ranker=ContinuousContinuousBFRanker(),
                reporter=ContinuousContinuousBFReporter(),
                path=self.path + "bruteforce/",
            )
        return analyses

    def __handle_predictors_with_cont_response(self) -> Dict[str, Analysis]:
        analyses = dict()
        if self.dataset.categorical_X is not None:
            analyses["categorical"] = Analysis(
                dataset=self.dataset,
                plotter=CategoricalXContinuousYPlotter(),
                ranker=CategoricalXContinuousYRanker(),
                reporter=CategoricalXContinuousYReporter(),
                path=self.path + "predictors/",
            )
        if self.dataset.continuous_X is not None:
            analyses["continuous"] = Analysis(
                dataset=self.dataset,
                plotter=ContinuousXContinuousYPlotter(),
                ranker=ContinuousXContinuousYRanker(),
                reporter=ContinuousXContinuousYReporter(),
                path=self.path + "predictors/",
            )
        return analyses

    def __handle_predictors_with_bool_response(self) -> Dict[str, Analysis]:
        analyses = dict()
        if self.dataset.categorical_X is not None:
            analyses["categorical"] = Analysis(
                dataset=self.dataset,
                plotter=CategoricalXBooleanYPlotter(),
                ranker=CategoricalXBooleanYRanker(),
                reporter=CategoricalXBooleanYReporter(),
                path=self.path + "predictors/",
            )
        if self.dataset.continuous_X is not None:
            analyses["continuous"] = Analysis(
                dataset=self.dataset,
                plotter=ContinuousXBooleanYPlotter(),
                ranker=ContinuousXBooleanYRanker(),
                reporter=ContinuousXBooleanYReporter(),
                path=self.path + "predictors/",
            )
        return analyses

    def __handle_response(self) -> Dict[str, Analysis]:
        if self.dataset.y_type == "continuous":
            return self.__handle_predictors_with_cont_response()
        elif self.dataset.y_type == "boolean":
            return self.__handle_predictors_with_bool_response()
        else:
            msg = f'Dataset has unsupported response type "{self.dataset.y}"'
            raise ValueError(msg)
