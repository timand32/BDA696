"""
"""
import sys
import webbrowser

import bins
import data
import metrics
import models
import plot
import report


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

    # Report predictors
    report.report_predictors(
        X0_metrics,
        "predictor_report.html",
        "./output/hw5/100-day/",
    )
    report.report_predictors(
        X1_metrics,
        "predictor_report.html",
        "./output/hw5/career/",
    )

    # Open report's folder in browser
    webbrowser.open("output/hw5/100-day/predictor_report.html", new=2)
    webbrowser.open("output/hw5/career/predictor_report.html", new=2)

    # Calculate correlations
    X0_corrs = metrics.calculate_correlations(X0)
    X1_corrs = metrics.calculate_correlations(X1)
    print(f"{X0_corrs}\n{X1_corrs}\n")

    # Plot correlations
    figure = plot.plot_correlations(X0_corrs)
    plot.save_figure(
        figure,
        "./output/hw5/100-day/plots/corr_plot.html",
    )
    figure = plot.plot_correlations(X1_corrs)
    plot.save_figure(
        figure,
        "./output/hw5/career/plots/corr_plot.html",
    )

    # Report correlations
    report.report_correlations(
        X0_corrs,
        "corr_report.html",
        "./output/hw5/100-day/",
    )
    report.report_correlations(
        X1_corrs,
        "corr_report.html",
        "./output/hw5/career/",
    )

    webbrowser.open("output/hw5/100-day/corr_report.html", new=2)
    webbrowser.open("output/hw5/career/corr_report.html", new=2)

    # Calculate brute-force
    X0_bf_bins = bins.bin_combinations(X0, y, n=5)
    X1_bf_bins = bins.bin_combinations(X1, y, n=5)

    # Plot bfs
    for key, b in X0_bf_bins.items():
        figure = plot.plot_bruteforce(b, key[0], key[1])
        plot.save_figure(
            figure,
            f"./output/hw5/100-day/plots/{key[0]}X{key[1]}_bf_plot.html",
        )
    for key, b in X1_bf_bins.items():
        figure = plot.plot_bruteforce(b, key[0], key[1])
        plot.save_figure(
            figure,
            f"./output/hw5/career/plots/{key[0]}X{key[1]}_bf_plot.html",
        )

    # Rank bfs
    X0_bf_ranks = metrics.rank_bf(X0_bf_bins)
    X1_bf_ranks = metrics.rank_bf(X1_bf_bins)

    # Report bfs
    report.report_bruteforces(
        X0_bf_ranks,
        "bf_report.html",
        "./output/hw5/100-day/",
    )
    report.report_bruteforces(
        X1_bf_ranks,
        "bf_report.html",
        "./output/hw5/career/",
    )

    webbrowser.open("output/hw5/100-day/bf_report.html", new=2)
    webbrowser.open("output/hw5/career/bf_report.html", new=2)

    # Build models
    features = [
        "s9_difference",
        "h9_difference",
        "ip_ratio",
        "hr9_difference",
    ]
    print("Model from 100-day stats:")
    models.build_models(X0[features], y)
    print("Model from prior career stats:")
    models.build_models(X1[features], y)
    print("A linearSVC appeard to perform slightly better than an RFC.")
    print("100-day rolling stats and career stats appear to perform the same.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
