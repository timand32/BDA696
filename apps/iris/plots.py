"""Module for generating plots of the Iris data set.
"""
import sys

import data
import pandas as pd


def generate_plots(iris_df: pd.DataFrame):
    return list()


def main() -> int:
    iris_df = data.load_data()
    plots = generate_plots(iris_df=iris_df)
    for plot in plots:
        print(plot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
