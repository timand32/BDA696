"""
"""
import pandas as pd


def bin_predictor(
    x: pd.Series,
    y: pd.Series,
    n: int = 10,
):
    df = x.to_frame()
    df[y.name] = y
    df["interval"] = pd.cut(x=df[x.name], bins=n)
    bins = pd.DataFrame()
    bins["lower_bin"] = (
        df.groupby("interval")["interval"].first().apply(lambda x: x.left)
    )
    bins["upper_bin"] = (
        df.groupby("interval")["interval"].first().apply(lambda x: x.right)
    )
    bins["bin_center"] = df.groupby("interval")[x.name].median()
    bins["bin_count"] = df.groupby("interval")[y.name].count()
    bins["bin_mean"] = df.groupby("interval")[y.name].mean()
    bins["pop_mean"] = y.mean()
    bins["pop_count"] = y.count()
    bins["mean_squared_diff"] = (bins["bin_mean"] - bins["pop_mean"]) ** 2
    bins["population_proportion"] = bins["bin_count"] / bins["pop_count"]
    bins["mean_squared_diff_weighted"] = (
        bins["population_proportion"] * bins["mean_squared_diff"]
    )
    return bins


if __name__ == "__main__":
    x = pd.Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], name="x")
    y = pd.Series([0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1], name="y")
    print(bin_predictor(x, y, n=5))
