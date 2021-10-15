"""Module importing several datasets.

Meant mostly for testing purposes.
"""

import sys

import seaborn

mpg = seaborn.load_dataset(name="mpg")
tips = seaborn.load_dataset(name="tips")
titanic = seaborn.load_dataset(name="titanic")

test_cases = [
    (
        mpg,
        [
            "cylinders",
            "displacement",
            "horsepower",
            "weight",
            "acceleration",
            "origin",
        ],
        "mpg",
    ),
    (
        tips,
        [
            "total_bill",
            "sex",
            "smoker",
            "day",
            "time",
            "size",
        ],
        "tip",
    ),
    (
        titanic,
        [
            "pclass",
            "sex",
            "age",
            "sibsp",
            "embarked",
            "class",
        ],
        "survived",
    ),
]
"""Test cases for feature score application.

(df, predictors, response)
"""


def main() -> int:
    for df, predictors, response in test_cases:
        features = list() + predictors
        features.append(response)
        print(df[features])
    return 0


if __name__ == "__main__":
    sys.exit(main())
