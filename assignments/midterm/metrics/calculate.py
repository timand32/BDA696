import pandas as pd

from .cont_pred_cont_resp import calculate_cont_pred_cont_resp_metrics


def calculate_feature_metrics(
    data_df: pd.DataFrame,
    feature_df: pd.DataFrame,
) -> pd.DataFrame:
    metric_df = pd.DataFrame()
    feature_df.reset_index()
    feature_df = feature_df.set_index("feature")
    resp_loc = feature_df.loc[feature_df["is_response"], :]
    for r_name in resp_loc.index:
        r_type = resp_loc.loc[r_name, "feature_type"]
        if r_type == "boolean":
            pass
        elif r_type == "continuous":
            cont_loc = feature_df.loc[
                (feature_df["feature_type"] == "continuous")
                | (feature_df["is_response"]),
                :,
            ]
            metric_df = metric_df.append(
                calculate_cont_pred_cont_resp_metrics(
                    data_df[cont_loc.index],
                    r_name,
                ),
                ignore_index=True,
            )
        else:
            raise ValueError(
                f"Feature {r_name} has unknown feature type {r_type}",
            )
    return metric_df
