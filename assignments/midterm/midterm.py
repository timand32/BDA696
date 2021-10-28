import sys
import webbrowser

import data
from analyzer import Analyzer


def main() -> int:
    title = "mpg"
    dataset = data.get_dataset(title)
    analyzer = Analyzer(dataset=dataset, path="output/")
    with open(f"output/{title}/index.html", "w+") as file:
        # https://www.w3schools.com/howto/howto_html_include.asp
        index = """<!DOCTYPE html>
            <html>
                <h1>BDA696 Midterm</h1>
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
    predictor_analyses = analyzer.analyze_predictors()  # noqa
    print("Predictor Analyses")
    print("=" * 20)
    for key, analysis in predictor_analyses.items():
        print(key)
        print(analysis)
        print()
    with open(f"output/{title}/predictors/index.html", "w+") as file:
        # https://www.w3schools.com/howto/howto_html_include.asp
        index = """<!DOCTYPE html>
            <html>
                <h1>Predictor Analyses</h1>
                <p><b>'File not found' if predictor doesn't exist.</b></p>
                <h1>Correlation Analyses</h1>
                <a target="_blank" href='reports/cat_pred_report.html'>
                    <h2>Categorical Predictor Rankings</h2>
                </a>
                <hline>
                <a target="_blank" href='reports/cont_pred_report.html'>
                    <h2>Continuous Predictor Rankings</h2>
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
        # https://www.w3schools.com/howto/howto_html_include.asp
        index = """<!DOCTYPE html>
            <html>
                <h1>Correlation Analyses</h1>
                <p><b>'File not found' if combination doesn't exist.</b></p>
                <h1>Correlation Analyses</h1>
                <a target="_blank" href='reports/cat_cat_corr_report.html'>
                    <h2>Categorical-Categorical Correlation Rankings</h2>
                </a>
                <hline>
                <a target="_blank" href='reports/cat_cont_corr_report.html'>
                    <h2>Categorical-Continuous Correlation Rankings</h2>
                </a>
                <hline>
                <a target="_blank" href='reports/cont_cont_corr_report.html'>
                    <h2>Continuous-Continuous Correlation Rankings</h2>
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
        # https://www.w3schools.com/howto/howto_html_include.asp
        index = """<!DOCTYPE html>
            <html>
                <p><b>'File not found' if combination doesn't exist.</b></p>
                <h1>Brute Force Analyses</h1>
                <a target="_blank" href='reports/cat_cat_bf_report.html'>
                    <h2>Categorical-Categorical Brute Force Rankings</h2>
                </a>
                <hline>
                <a target="_blank" href='reports/cat_cont_bf_report.html'>
                    <h2>Categorical-Continuous Brute Force Rankings</h2>
                </a>
                <hline>
                <a target="_blank" href='reports/cont_cont_bf_report.html'>
                    <h2>Continuous-Continuous Brute Force Rankings</h2>
                </a>
                <hline>
            </html>
        """
        file.write(index)
    webbrowser.open(f"output/{dataset.title}/index.html", new=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
