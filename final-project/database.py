"""
"""
# import pandas as pd
import pandas as pd
import sqlalchemy

"""Constants used to access database.
"""
DB_USER = "root"
DB_PASS = "password"  # pragma: allowlist secret
DB_HOST = "mariadb:3306"
DB_DATABASE = "baseball"
DB_URL = "mariadb+mariadbconnector://"
DB_URL += f"{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_DATABASE}"

SQL_ENGINE = sqlalchemy.create_engine(DB_URL)


def get_response() -> pd.Series:
    query = """
    SELECT
        game_id,
        home_won
    FROM
        team_performance
    WHERE
        is_home = 1
    """
    df = pd.read_sql_query(query, SQL_ENGINE)
    df = df.set_index("game_id")
    df = df.sort_index()
    series = df["home_won"]
    return series


RESPONSE = get_response()
AVERAGE_WINS = RESPONSE.mean()


def get_dips_X() -> pd.DataFrame:
    query0 = """
    SELECT
        *
    FROM
        starter_dips_roll160
    """
    X0 = pd.read_sql_query(query0, SQL_ENGINE)
    X0 = X0.set_index("game_id")
    mapper0 = {c: c + "_sp_roll160" for c in X0.columns}
    X = X0.rename(mapper=mapper0, axis=1)

    return X


def get_bsr_X() -> pd.DataFrame:
    query0 = """
    SELECT
        *
    FROM
        bsr_career
    """
    X0 = pd.read_sql_query(query0, SQL_ENGINE)
    X0 = X0.drop(["win", "home_id", "is_home"], axis=1)
    X0 = X0.set_index("game_id")
    mapper0 = {c: c + "_career" for c in X0.columns}
    X = X0.rename(mapper=mapper0, axis=1)

    for i in [10, 160, 320]:
        query = f"""
        SELECT
            *
        FROM
            bsr_roll{i}
        """
        other = pd.read_sql_query(query, SQL_ENGINE)
        other = other.drop(["win", "home_id", "is_home"], axis=1)
        other = other.set_index("game_id")
        mapper = {c: c + f"_roll{i}" for c in X0.columns}
        other = other.rename(mapper=mapper, axis=1)
        X = X.join(other)

    return X


def get_pythagorean_X() -> pd.DataFrame:
    query0 = """
    SELECT
        *
    FROM
        pyth_career
    """
    X0 = pd.read_sql_query(query0, SQL_ENGINE)
    X0 = X0.drop(["home_won", "home_id", "away_id"], axis=1)
    X0 = X0.set_index("game_id")
    mapper0 = {c: c + "_career" for c in X0.columns}
    X = X0.rename(mapper=mapper0, axis=1)

    for i in [10, 160, 320]:
        query = f"""
        SELECT
            *
        FROM
            pyth_roll{i}
        """
        other = pd.read_sql_query(query, SQL_ENGINE)
        other = other.drop(["home_won", "home_id", "away_id"], axis=1)
        other = other.set_index("game_id")
        mapper = {c: c + f"_roll{i}" for c in X0.columns}
        other = other.rename(mapper=mapper, axis=1)
        X = X.join(other)

    return X


def get_all_X() -> pd.DataFrame:
    X0 = get_pythagorean_X()
    X0 = X0.drop(
        X0.columns.difference(
            [
                "pyth1_diff_roll160",
                "home_pyth2_roll160",
                "away_pyth2_roll320",
            ]
        ),
        axis=1,
    )
    X = X0
    X1 = get_bsr_X()
    X1 = X1.drop(
        X1.columns.difference(
            [
                "simple_ratio_roll160",
                "simple_ratio_roll10",
                "away_offshoot_career",
            ]
        ),
        axis=1,
    )
    X = X.join(X1)
    X2 = get_dips_X()
    X2 = X2.drop(
        X2.columns.difference(
            [
                "dice_diff_sp_roll160",
                "away_dice_sp_roll160",
                "home_dice_sp_roll160",
            ]
        ),
        axis=1,
    )
    X = X.join(X2)

    return X
