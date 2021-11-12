"""
"""
import sys
import webbrowser

import data
import plot


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
    # Log this instead, eventually
    print(f"{y}\n{X0}\n{X1}")

    # Plot feature distribution by response
    for _, x in X0.items():
        figure = plot.plot_violin(x, y, "100-day rolling")
        plot.save_figure(
            figure,
            f"./output/hw5/100-day/plots/feature_{x.name}_100_day_plot.html",
        )
    for _, x in X1.items():
        figure = plot.plot_violin(x, y, "prior career")
        plot.save_figure(
            figure,
            f"./output/hw5/career/plots/feature_{x.name}_career_plot.html",
        )

    # Calculate and score metrics for each predictor
    # Open report's folder in browser
    webbrowser.open("output/hw5/", new=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
