"""Module for building and scoring plots of the Iris data set.
"""

import sys

import data
import pandas as pd
import sklearn.ensemble as sklensemble
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

seed = 42
"""Seed number for random states in models."""


def _build_randomforest_pipeline() -> Pipeline:
    # Build a Random Forest Classifier Pipeline
    rfc_pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("rfc", sklensemble.RandomForestClassifier(random_state=seed)),
        ]
    )
    return rfc_pipeline


def _build_gradientboosting_pipeline() -> Pipeline:
    # Build a Gradient Boosting Classifier Pipeline
    gbc_pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("gbc", sklensemble.GradientBoostingClassifier(random_state=seed)),
        ]
    )
    return gbc_pipeline


def _build_adaboost_pipeline() -> Pipeline:
    # Build a AdaBoost Classifier Pipeline
    abc_pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("abc", sklensemble.AdaBoostClassifier(random_state=seed)),
        ]
    )
    return abc_pipeline


def build_pipelines() -> list:
    # Build all supported pipelines
    pipelines = list()
    pipelines.append(_build_randomforest_pipeline())
    pipelines.append(_build_gradientboosting_pipeline())
    pipelines.append(_build_adaboost_pipeline())
    return pipelines


def train_pipelines(iris_df: pd.DataFrame, pipelines: list) -> list:
    # Trains and returns a list of pipelines
    trained_pipelines = list()
    x_matrix = iris_df[data.continuous_feature_list]
    y_list = iris_df["class"].values
    for pipeline in pipelines:
        trained_pipelines.append(pipeline.fit(X=x_matrix, y=y_list))
    return trained_pipelines


def analyze_pipelines(iris_df: pd.DataFrame, pipelines: list) -> None:
    for pipeline in pipelines:
        print(f"Pipeline: {pipeline}")
        x_matrix = iris_df[data.continuous_feature_list]
        y_list = iris_df["class"].values
        predictions = pipeline.predict(x_matrix)
        probabilities = pipeline.predict_proba(x_matrix)
        for i, _ in enumerate(predictions):
            print(f"{i}:{predictions[i]},{probabilities[i]}")
        score = pipeline.score(x_matrix, y_list)
        print(f"Estimator score: {score}")


def main() -> int:
    iris_df = data.load_data()
    # Build models
    pipelines = build_pipelines()
    pipelines = train_pipelines(iris_df, pipelines)
    # Score models
    analyze_pipelines(iris_df, pipelines)
    return 0


if __name__ == "__main__":
    sys.exit(main())
