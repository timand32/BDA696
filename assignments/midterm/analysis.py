"""
"""

from data import Dataset
from plotter import Plotter
from ranker import Ranker
from reporter import Reporter


class Analysis(object):
    """Class for encapsulating an analysis."""

    def __init__(
        self,
        dataset: Dataset,
        plotter: Plotter,
        ranker: Ranker,
        reporter: Reporter,
        path: str,
    ):
        self.dataset = dataset
        self.ranker: Ranker = ranker
        self.rank_df = ranker.rank(dataset=self.dataset)
        self.plotter: Plotter = plotter
        self.plot_df = plotter.plot(
            dataset=self.dataset,
            rank_df=self.rank_df,
            path=path,
        )
        self.reporter: Reporter = reporter
        self.report_df = reporter.report(
            dataset=self.dataset,
            plot_df=self.plot_df,
            rank_df=self.rank_df,
            path=path,
        )

    def __str__(self):
        return (
            "plot_df:\n"
            + f"{self.plot_df}\n"
            + "rank_df:\n"
            + f"{self.rank_df}\n"
            + "report_df:\n"
            + f"{self.report_df}\n"
        )
