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
    X0 = data.load_pythagorean()
    # make sure we only keep y we have X for.
    y = y.loc[y.index.isin(X0.index)]
    # same for X with y
    X0 = X0.loc[X0.index.isin(y.index)]
    # Log this instead, eventually
    print(f"{y}\n{X0}")

    # Plot feature distribution by response
    for _, x in X0.items():
        figure = plot.plot_violin(x, y, "100-day rolling")
        plot.save_figure(
            figure,
            f"./output/hw5/pythagorean/plots/{x.name}_feature_plot.html",
        )

    # Bin the responses into n=10 populations.
    X0_bins = {x.name: bins.bin_predictor(x, y) for _, x in X0.items()}
    print(f"{X0_bins}\n")

    # Plot weighted and unweighted
    for _, x in X0.items():
        figure = plot.plot_bins(x.name, y.name, X0_bins[x.name])
        plot.save_figure(
            figure,
            f"./output/hw5/pythagorean/plots/{x.name}_bin_plot.html",
        )

    # Calculate and score metrics for each predictor
    X0_metrics = metrics.calculate_predictor_metrics(X0, X0_bins, y)
    print(f"{X0_metrics}\n")

    # Report predictors
    report.report_predictors(
        X0_metrics,
        "predictor_report.html",
        "./output/hw5/pythagorean/",
    )

    # Open report's folder in browser
    webbrowser.open("output/hw5/pythagorean/predictor_report.html", new=2)

    # Calculate correlations
    X0_corrs = metrics.calculate_correlations(X0)
    print(f"{X0_corrs}\n")

    # Plot correlations
    figure = plot.plot_correlations(X0_corrs)
    plot.save_figure(
        figure,
        "./output/hw5/pythagorean/plots/corr_plot.html",
    )

    # Report correlations
    report.report_correlations(
        X0_corrs,
        "corr_report.html",
        "./output/hw5/pythagorean/",
    )

    webbrowser.open("output/hw5/pythagorean/corr_report.html", new=2)

    # Calculate brute-force
    X0_bf_bins = bins.bin_combinations(X0, y, n=5)

    # Plot bfs
    for key, b in X0_bf_bins.items():
        figure = plot.plot_bruteforce(b, key[0], key[1])
        plot.save_figure(
            figure,
            f"./output/hw5/pythagorean/plots/{key[0]}X{key[1]}_bf_plot.html",
        )

    # Rank bfs
    X0_bf_ranks = metrics.rank_bf(X0_bf_bins, X0_corrs)

    # Report bfs
    report.report_bruteforces(
        X0_bf_ranks,
        "bf_report.html",
        "./output/hw5/pythagorean/",
    )

    webbrowser.open("output/hw5/pythagorean/bf_report.html", new=2)

    # Build models
    features = ["diff_smyth"]
    print("Model from pythagorean stats:")
    models.build_models(X0[features], y)
    print("A linearSVC appeard to perform slightly better than an RFC.")
    print("100-day rolling stats and career stats appear to perform the same.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
