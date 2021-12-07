"""Module for Iris application (BDA696 Assignmnent #1)
"""

import sys

import data
import models
import plots


def main() -> int:
    iris_df = data.load_data()
    print(iris_df)
    iris_desc = data.describe_data(iris_df)
    print(iris_desc)
    iris_plots = plots.generate_plots(iris_df)
    for plot in iris_plots:
        plot.show(validate=False)
    pipelines = models.build_pipelines()
    pipelines = models.train_pipelines(iris_df, pipelines)
    models.analyze_pipelines(iris_df, pipelines)
    return 0


if __name__ == "__main__":
    sys.exit(main())
