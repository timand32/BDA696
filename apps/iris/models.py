"""Module for building and scoring plots of the Iris data set.
"""

import sys

import data


def main() -> int:
    iris_df = data.load_data()
    print(iris_df)  # temp
    # Build models
    # Score models
    return 0


if __name__ == "__main__":
    sys.exit(main())
