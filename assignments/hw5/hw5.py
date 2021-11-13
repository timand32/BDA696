"""
"""
import sys
import webbrowser

import bins
import data
import metrics
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
            f"./output/hw5/100-day/plots/{x.name}_feature_plot.html",
        )
    for _, x in X1.items():
        figure = plot.plot_violin(x, y, "prior career")
        plot.save_figure(
            figure,
            f"./output/hw5/career/plots/{x.name}_feature_plot.html",
        )

    # Bin the responses into n=10 populations.
    X0_bins = {x.name: bins.bin_predictor(x, y) for _, x in X0.items()}
    X1_bins = {x.name: bins.bin_predictor(x, y) for _, x in X1.items()}
    print(f"{X0_bins}\n{X1_bins}\n")

    # Plot weighted and unweighted
    for _, x in X0.items():
        figure = plot.plot_bins(x.name, y.name, X0_bins[x.name])
        plot.save_figure(
            figure,
            f"./output/hw5/100-day/plots/{x.name}_bin_plot.html",
        )
    for _, x in X1.items():
        figure = plot.plot_bins(x.name, y.name, X1_bins[x.name])
        plot.save_figure(
            figure,
            f"./output/hw5/career/plots/{x.name}_bin_plot.html",
        )

    # Calculate and score metrics for each predictor
    X0_metrics = metrics.calculate_predictor_metrics(X0, X0_bins, y)
    X1_metrics = metrics.calculate_predictor_metrics(X1, X1_bins, y)
    print(f"{X0_metrics}\n{X1_metrics}\n")

    # Open report's folder in browser
    webbrowser.open("output/hw5/", new=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
