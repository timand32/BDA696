"""
"""
import sys

import data


def main() -> int:
    # Load data
    y = data.load_y()
    X0 = data.load_rolling_100_pitcher_X()
    X1 = data.load_prior_career_pitcher_X()
    # make sure we only keep y we have X for.
    y = y.loc[y.index.isin(X0.index)]
    # same for X with y
    X0 = X0.loc[X0.index.isin(y.index)]
    X1 = X1.loc[X1.index.isin(y.index)]
    print(f"{y}\n{X0}\n{X1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
