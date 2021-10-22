"""Modules for wrapping everything into a html report.
"""
import sys
from pathlib import Path

import data
import pandas as pd
import plots
import ranks
import scores


def generate_report(
    title: str,
    df: pd.DataFrame,
    predictors: list[str],
    response: str,
) -> None:
    PATH = f"output/{title}/"
    f = plots.plot_dataset(df, response, predictors)
    plots.save_plots(f, PATH + "plots/")
    s = scores.score_dataframe(df, predictors, response)
    r = ranks.rank_scores(s)
    # Add columns for plots
    r["heatmap"] = None
    for pred, _ in r.iterrows():
        pth = f"plots/{r['predictor'][pred]}/heatmap.html"
        if Path(PATH + pth).exists():
            r["heatmap"][pred] = pth
    r["histogram"] = None
    for pred, _ in r.iterrows():
        pth = f"plots/{r['predictor'][pred]}/histogram.html"
        if Path(PATH + pth).exists():
            r["histogram"][pred] = pth
    r["violin"] = None
    for pred, _ in r.iterrows():
        pth = f"plots/{r['predictor'][pred]}/violin.html"
        if Path(PATH + pth).exists():
            r["violin"][pred] = pth
    r["scatter"] = None
    for pred, _ in r.iterrows():
        pth = f"plots/{r['predictor'][pred]}/scatter.html"
        if Path(PATH + pth).exists():
            r["scatter"][pred] = pth
    r["diff"] = None
    for pred, _ in r.iterrows():
        pth = f"plots/{r['predictor'][pred]}/diff.html"
        if Path(PATH + pth).exists():
            r["diff"][pred] = pth
    # From pandas docs
    link = '<a target="_blank" href="{0}">{0}</a>'
    sty = r.style.format(
        {
            "heatmap": link,
            "histogram": link,
            "violin": link,
            "scatter": link,
            "diff": link,
        },
        escape="html",
        na_rep="NA",
    )
    # Stack Overflow Q#64812819
    # Styler doesn't come with lines, had to add them.
    sty = sty.set_table_styles(
        [
            {"selector": "", "props": [("border", "1px solid grey")]},
            {"selector": "tbody td", "props": [("border", "1px solid grey")]},
            {"selector": "th", "props": [("border", "1px solid grey")]},
        ]
    )
    r_html = sty.render(escape=False)
    with open(f"{PATH}index.html", "w+") as file:
        file.write(r_html)
    return None


def main() -> int:
    df, predictors, response = data.test_cases[0]
    generate_report("mpg", df, predictors, response)
    df, predictors, response = data.test_cases[1]
    generate_report("tips", df, predictors, response)
    df, predictors, response = data.test_cases[2]
    generate_report("titanic", df, predictors, response)
    return 0


if __name__ == "__main__":
    sys.exit(main())
