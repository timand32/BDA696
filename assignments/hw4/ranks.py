"""Module for ranking plots together.
"""

import sys

import data
import pandas as pd
import scores


def rank_scores(score_dict: dict[dict[str, float]]) -> dict[pd.DataFrame]:
    sdf = pd.DataFrame()
    # Get scores into a table
    for key in score_dict:
        score_dict[key] = {
            **{"predictor": key},
            **score_dict[key],
        }
        sdf = sdf.append(score_dict[key], True)
    # Rank continuous scores
    cont_df = sdf[sdf["type"] == "continuous"].dropna(axis=1)
    cont_df = cont_df.set_index(["predictor", "type"])
    # Ranking scheme: normalize scores,
    # Average them out, then use that score to rank.
    for col in cont_df.columns:
        cont_df[col] = cont_df[col].astype(float)
        cont_df[col] = cont_df[col].abs()
        cont_df[col] = cont_df[col] / cont_df[col].max()
    cont_df["overall_score"] = cont_df.sum(axis=1, numeric_only=True) / len(
        cont_df.columns
    )
    cont_df = cont_df.reset_index()
    cont_df = cont_df.set_index(["predictor"])
    # Rank categorical scores
    cat_df = sdf[sdf["type"] == "categorical"].dropna(axis=1)
    cat_df = cat_df.set_index(["predictor", "type"])
    for col in cat_df.columns:
        cat_df[col] = cat_df[col].astype(float)
        cat_df[col] = cat_df[col].abs()
        cat_df[col] = cat_df[col] / cat_df[col].max()
    cat_df["overall_score"] = cat_df.sum(axis=1, numeric_only=True) / len(
        cat_df.columns
    )
    cat_df = cat_df.reset_index()
    cat_df = cat_df.set_index(["predictor"])
    # Add to main df
    new_df = cont_df.append(cat_df)
    sdf = sdf.set_index(["predictor"])
    sdf = sdf.merge(
        new_df["overall_score"],
        left_index=True,
        right_index=True,
    )
    sdf = sdf.reset_index()
    sdf = sdf.sort_values(by=["type", "overall_score"], ascending=False)
    return sdf


def main() -> int:
    score_dict_list = list()
    for df, _, response in data.test_cases:
        predictors = [str(c) for c in df.columns if c != response]
        score_dict_list.append(
            scores.score_dataframe(df, predictors, response),
        )
    for sdict in score_dict_list:
        print(rank_scores(sdict))


if __name__ == "__main__":
    sys.exit(main())
