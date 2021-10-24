"""Main app module for midterm."""

import sys

import data
import metrics
import plotting
import preprocessing


def main() -> int:
    return 0


if __name__ == "__main__":
    data_df, predictors, response = data.get_test_data_set("diabetes")
    data_df = preprocessing.subset_dataframe(data_df, predictors, response)
    feature_df = preprocessing.determine_feature_types(data_df, response)
    fig_df = plotting.plot_predictors(data_df, feature_df, "output/diabetes/")
    metric_df = metrics.calculate_feature_metrics(data_df, feature_df)
    sys.exit(main())
