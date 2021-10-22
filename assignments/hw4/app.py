"""Main app module for HW4.

Usage: change the parameters above.
"""
import sys
import webbrowser

import data
import pandas
import reports

TITLE: str = "mpg"
"""Title for report:
Effects what folder report gets output to.
"""
DF: pandas.DataFrame = data.mpg
"""Dataframe for report.
"""
PREDICTORS: list[str] = [
    "cylinders",
    "displacement",
    "horsepower",
    "weight",
    "acceleration",
    "origin",
]
"""Predictor list for report.
"""
RESPONSE: str = "mpg"
"""Response for report.
"""


def main() -> int:
    reports.generate_report(
        title=TITLE,
        df=DF,
        predictors=PREDICTORS,
        response=RESPONSE,
    )
    webbrowser.open(f"output/{TITLE}/index.html", new=2)


if __name__ == "__main__":
    sys.exit(main())
