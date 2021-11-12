"""
"""
import pandas as pd
import sqlalchemy

"""Constants used to access database.
"""
DB_USER = "root"
DB_PASS = "password"  # pragma: allowlist secret
DB_HOST = "localhost"
DB_DATABASE = "baseball"
DB_URL = "mariadb+mariadbconnector://"
DB_URL += f"{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_DATABASE}"

SQL_ENGINE = sqlalchemy.create_engine(DB_URL)


def load_y() -> pd.Series:
    query = """
    SELECT
        game_id,
        winner_home_or_away AS home_team_wins
    FROM
        boxscore
    """
    df = pd.read_sql_query(query, SQL_ENGINE)
    df = df.replace("H", 1)
    df = df.replace("A", 0)
    df = df.replace("", float("NaN"))
    df = df.dropna()
    df = df.set_index("game_id")
    df = df.sort_index()
    df = df.astype("int")
    series = df["home_team_wins"]
    return series


def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(
        labels=[
            "local_date",
            "home_pitcher",
            "away_pitcher",
        ],
        axis=1,
    )
    return df


def load_rolling_100_pitcher_X() -> pd.DataFrame:
    query = "SELECT * FROM starting_pitcher_stats_100"
    df = pd.read_sql_query(query, SQL_ENGINE)
    df = drop_columns(df)
    df = df.set_index("game_id")
    return df


def load_prior_career_pitcher_X() -> pd.DataFrame:
    query = "SELECT * FROM starting_pitcher_stats_prior_career"
    df = pd.read_sql_query(query, SQL_ENGINE)
    df = drop_columns(df)
    df = df.set_index("game_id")
    return df


if __name__ == "__main__":
    y = load_y()
    X0 = load_rolling_100_pitcher_X()
    X1 = load_prior_career_pitcher_X()
    print(f"{y}\n{X0}\n{X1}")
