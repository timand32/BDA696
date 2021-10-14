"""Module for determining feature types.
"""

import sys
from enum import Enum

import data
from pandas import Series


class FeatureType(Enum):
    CONTINUOUS = 0
    CATEGORICAL = 1
    BOOLEAN = 2


def determine_response_type(feature: Series) -> FeatureType:
    """Continuous or boolean."""
    # If there are only two values in response,
    # we know it's boolean.
    if len(feature.unique()) == 2:
        return FeatureType.BOOLEAN
    # Otherwise, we can assume its continuous
    return FeatureType.CONTINUOUS


def determine_predictor_type(
    feature: Series,
    threshold: float = 0.05,
) -> FeatureType:
    """Continuous or categorical."""
    # Assume category or object dtypes are categorical
    if feature.dtype.name in ["category", "object"]:
        return FeatureType.CATEGORICAL
    # Categories encoded in integers are tricky...
    # Found an answer in Stack Overflow Q #35826912
    # that gave a heuristic for guessing this.
    if float(feature.nunique()) / feature.count() < threshold:
        return FeatureType.CATEGORICAL
    # Otherwise, we can assume its continuous
    return FeatureType.CONTINUOUS


def main() -> int:
    for df, predictors, response in data.test_cases:
        response_type = determine_response_type(df[response])
        print(f"Response {response} is {response_type}")
        for i, p in enumerate(predictors):
            predictor_type = determine_predictor_type(df[p])
            print(f"{i:02} Predictor {p} is {predictor_type}")


if __name__ == "__main__":
    sys.exit(main())
