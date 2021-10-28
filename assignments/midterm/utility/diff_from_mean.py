"""
"""
import pandas


def create_2D_cat_diff_from_mean_table(
    X: pandas.DataFrame,
    y: pandas.Series,
) -> pandas.DataFrame:
    diff_df = pandas.DataFrame()
    x0name = X.columns[0]
    x1name = X.columns[1]
    yname = y.name
    x0 = X[x0name]
    x1 = X[x1name]
    X[yname] = y
    pop_count = y.count()
    pop_mean = y.mean()
    for j, j_category in enumerate(
        x1.sort_values().unique(),
    ):
        for i, i_category in enumerate(
            x0.sort_values().unique(),
        ):
            x0mask = X[x0name] == (i_category)
            x1mask = X[x1name] == (j_category)
            bin_data = X.loc[(x0mask) & (x1mask), :]
            if len(bin_data) > 0:
                diff_df = diff_df.append(
                    {
                        "i": i,
                        "j": j,
                        "i_category": i_category,
                        "j_category": j_category,
                        "total_pop": pop_count,
                        "total_mean": pop_mean,
                        "bin_pop": bin_data[yname].count(),
                        "bin_w": (bin_data[yname].count() / pop_count),
                        "bin_mean": bin_data[yname].mean(),
                        "dmr": (bin_data[yname].mean() - pop_mean),
                        "dmrsq": (bin_data[yname].mean() - pop_mean) ** 2,
                    },
                    ignore_index=True,
                )
            else:
                diff_df = diff_df.append(
                    {
                        "i": i,
                        "j": j,
                        "i_category": i_category,
                        "j_category": j_category,
                        "total_pop": pop_count,
                        "total_mean": pop_mean,
                        "bin_pop": 0,
                        "bin_w": 0,
                        "bin_mean": None,
                        "dmr": None,
                        "dmrsq": None,
                    },
                    ignore_index=True,
                )
    return diff_df


def create_2D_cat_cont_diff_from_mean_table(
    X: pandas.DataFrame,
    y: pandas.Series,
    n: int = 10,
) -> pandas.DataFrame:
    diff_df = pandas.DataFrame()
    x0name = X.columns[0]
    x1name = X.columns[1]
    yname = y.name
    x0 = X[x0name]
    x1 = X[x1name]
    X[yname] = y
    X["j_interval"] = pandas.cut(x=x1, bins=n)
    pop_count = y.count()
    pop_mean = y.mean()
    for j, j_interval in enumerate(
        X["j_interval"].sort_values().unique(),
    ):
        for i, i_category in enumerate(
            x0.sort_values().unique(),
        ):
            x0mask = X[x0name] == (i_category)
            x1mask = X[x1name].apply(lambda x: x in j_interval)
            bin_data = X.loc[(x0mask) & (x1mask), :]
            if len(bin_data) > 0:
                diff_df = diff_df.append(
                    {
                        "i": i,
                        "j": j,
                        "i_category": i_category,
                        "j_interval": j_interval,
                        "total_pop": pop_count,
                        "total_mean": pop_mean,
                        "bin_pop": bin_data[yname].count(),
                        "bin_w": (bin_data[yname].count() / pop_count),
                        "bin_mean": bin_data[yname].mean(),
                        "dmr": (bin_data[yname].mean() - pop_mean),
                        "dmrsq": (bin_data[yname].mean() - pop_mean) ** 2,
                    },
                    ignore_index=True,
                )
            else:
                diff_df = diff_df.append(
                    {
                        "i": i,
                        "j": j,
                        "i_category": i_category,
                        "j_interval": j_interval,
                        "total_pop": pop_count,
                        "total_mean": pop_mean,
                        "bin_pop": 0,
                        "bin_w": 0,
                        "bin_mean": None,
                        "dmr": None,
                        "dmrsq": None,
                    },
                    ignore_index=True,
                )
    return diff_df


def create_2D_cont_diff_from_mean_table(
    X: pandas.DataFrame,
    y: pandas.Series,
    n: int = 10,
) -> pandas.DataFrame:
    diff_df = pandas.DataFrame()
    x0name = X.columns[0]
    x1name = X.columns[1]
    yname = y.name
    x0 = X[x0name]
    x1 = X[x1name]
    X[yname] = y
    X["i_interval"] = pandas.cut(x=x0, bins=n)
    X["j_interval"] = pandas.cut(x=x1, bins=n)
    pop_count = y.count()
    pop_mean = y.mean()
    for j, j_interval in enumerate(
        X["j_interval"].sort_values().unique(),
    ):
        for i, i_interval in enumerate(
            X["i_interval"].sort_values().unique(),
        ):
            x0mask = X[x0name].apply(lambda x: x in i_interval)
            x1mask = X[x1name].apply(lambda x: x in j_interval)
            bin_data = X.loc[(x0mask) & (x1mask), :]
            if len(bin_data) > 0:
                diff_df = diff_df.append(
                    {
                        "i": i,
                        "j": j,
                        "i_interval": i_interval,
                        "j_interval": j_interval,
                        "total_pop": pop_count,
                        "total_mean": pop_mean,
                        "bin_pop": bin_data[yname].count(),
                        "bin_w": (bin_data[yname].count() / pop_count),
                        "bin_mean": bin_data[yname].mean(),
                        "dmr": (bin_data[yname].mean() - pop_mean),
                        "dmrsq": (bin_data[yname].mean() - pop_mean) ** 2,
                    },
                    ignore_index=True,
                )
            else:
                diff_df = diff_df.append(
                    {
                        "i": i,
                        "j": j,
                        "i_interval": i_interval,
                        "j_interval": j_interval,
                        "total_pop": pop_count,
                        "total_mean": pop_mean,
                        "bin_pop": 0,
                        "bin_w": 0,
                        "bin_mean": None,
                        "dmr": None,
                        "dmrsq": None,
                    },
                    ignore_index=True,
                )
    return diff_df
