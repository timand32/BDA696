import sys
import webbrowser

import data
from analyzer import Analyzer

TITLE = "diabetes"
"""Determines dataset that gets reported.

To change target dataset, pass its title as a string.

To target a random dataset, pass None.

To add new datasets, modify the `get_data` function in ./data/
"""


def main() -> int:
    title = TITLE
    dataset = data.get_dataset(title)
    if title is None:
        title = dataset.title
    # In a perfect world, probably would want to include in Dataset class.
    n_categorical = len(dataset.categorical_X.columns)
    n_continuous = len(dataset.continuous_X.columns)
    n_cat_cat = len(dataset.X_combinations[("categorical", "categorical")])
    n_cat_cont = len(dataset.X_combinations[("categorical", "continuous")])
    n_cont_cont = len(dataset.X_combinations[("continuous", "continuous")])

    analyzer = Analyzer(dataset=dataset, path="output/")
    predictor_analyses = analyzer.analyze_predictors()  # noqa
    with open(f"output/{title}/index.html", "w+") as file:
        index = f"""<!DOCTYPE html>
            <html>
                <h1>BDA696 Midterm ({title} dataset)</h1>
                    <h2>Counts</h2>
                    <p>Categorical Predictors: {n_categorical}</p>
                    <p>Continous Predictors: {n_continuous}</p>
                <a target="_blank" href='predictors/index.html'>
                    <h2>Predictor Analyses</h2>
                </a>
                <hline>
                <a target="_blank" href='correlations/index.html'>
                    <h2>Correlations Analyses</h2>
                </a>
                <a target="_blank" href='bruteforce/index.html'>
                    <h2>Brute Force Analyses</h2>
                </a>
                <hline>
            </html>
        """
        file.write(index)
    print("Predictor Analyses")
    print("=" * 20)
    for key, analysis in predictor_analyses.items():
        print(key)
        print(analysis)
        print()
    with open(f"output/{title}/predictors/index.html", "w+") as file:
        index = f"""<!DOCTYPE html>
            <html>
                <h1>{title} Predictor Analyses</h1>
                <p><b>File not Found since ranks not yet implemented.</b></p>
                <h1>Correlation Analyses</h1>
                <a target="_blank" href='reports/cat_pred_report.html'>
                    <h2>Categorical Predictor Rankings</h2>
                    <p>Categorical Predictors: {n_categorical}</p>
                </a>
                <hline>
                <a target="_blank" href='reports/cont_pred_report.html'>
                    <h2>Continuous Predictor Rankings</h2>
                    <p>Continous Predictors: {n_continuous}</p>
                </a>
                <hline>
            </html>
        """
        file.write(index)
    corr_analyses = analyzer.analyze_correlations()  # noqa
    print("Correlation Analyses")
    print("=" * 20)
    for key, analysis in corr_analyses.items():
        print(key)
        print(analysis)
        print()
    with open(f"output/{title}/correlations/index.html", "w+") as file:
        index = f"""<!DOCTYPE html>
            <html>
                <h1>{title} Correlation Analyses</h1>
                <p><b>'File not found' if 0 combinations</b></p>
                <h1>Correlation Analyses</h1>
                <a target="_blank" href='reports/cat_cat_corr_report.html'>
                    <h2>Categorical-Categorical Correlation Rankings</h2>
                    <p>Cat-Cat Predictors: {n_cat_cat}</p>
                </a>
                <hline>
                <a target="_blank" href='reports/cat_cont_corr_report.html'>
                    <h2>Categorical-Continuous Correlation Rankings</h2>
                    <p>Cat-Cont Predictors: {n_cat_cont}</p>
                </a>
                <hline>
                <a target="_blank" href='reports/cont_cont_corr_report.html'>
                    <h2>Continuous-Continuous Correlation Rankings</h2>
                    <p>Cont-Cont Predictors: {n_cont_cont}</p>
                </a>
                <hline>
            </html>
        """
        file.write(index)
    bf_analyses = analyzer.analyze_brute_force()  # noqa
    print("Brute Force Analyses")
    print("=" * 20)
    for key, analysis in bf_analyses.items():
        print(key)
        print(analysis)
        print()
    with open(f"output/{title}/bruteforce/index.html", "w+") as file:
        index = f"""<!DOCTYPE html>
            <html>
                <h1>{title} Brute Force Analyses</h1>
                <p><b>'File not found' if combination doesn't exist.</b></p>
                <a target="_blank" href='reports/cat_cat_bf_report.html'>
                    <h2>Categorical-Categorical Brute Force Rankings</h2>
                    <p>Cat-Cat Predictors: {n_cat_cat}</p>
                </a>
                <hline>
                <a target="_blank" href='reports/cat_cont_bf_report.html'>
                    <h2>Categorical-Continuous Brute Force Rankings</h2>
                    <p>Cat-Cont Predictors: {n_cat_cont}</p>
                </a>
                <hline>
                <a target="_blank" href='reports/cont_cont_bf_report.html'>
                    <h2>Continuous-Continuous Brute Force Rankings</h2>
                    <p>Cont-Cont Predictors: {n_cont_cont}</p>
                </a>
                <hline>
            </html>
        """
        file.write(index)
    webbrowser.open(f"output/{dataset.title}/index.html", new=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
