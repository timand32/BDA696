"""
"""
import pandas as pd
import sqlalchemy

"""Constants used to access database.
"""
DB_USER = "root"
DB_PASS = "password"  # pragma: allowlist secret
DB_HOST = "localhost:3306"
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


AVERAGE_WINS = load_y().mean()


def load_pythagorean() -> pd.DataFrame:
    df = pd.DataFrame()

    query = "SELECT * FROM career_pythagorean;"
    other = pd.read_sql_query(query, SQL_ENGINE)
    mapper = {c: f"{c}_career" for c in other.columns if c != "game_id"}
    other = other.rename(mapper=mapper, axis=1)
    df = df.append(other)
    df = df.set_index("game_id")

    query = "SELECT * FROM season_pythagorean;"
    other = pd.read_sql_query(query, SQL_ENGINE)
    mapper = {c: f"{c}_season" for c in other.columns if c != "game_id"}
    other = other.rename(mapper=mapper, axis=1)
    other = other.set_index("game_id")
    df = df.join(other)

    for i in [1]:  # [1, 8, 13, 55, 144, ]:
        query = f"CALL rolling_pythagorean({i});"
        other = pd.read_sql_query(query, SQL_ENGINE)
        mapper = {c: f"{c}_{i}" for c in other.columns if c != "game_id"}
        other = other.rename(mapper=mapper, axis=1)
        other = other.set_index("game_id")
        df = df.join(other=other)

    return df


def load_183() -> pd.DataFrame:
    query = "CALL pythagorean(100)"
    df = pd.read_sql_query(query, SQL_ENGINE)
    df = df.set_index("game_id")
    return df


def load_smyth():
    query = "CALL pythagorean_smyth(1000)"
    df = pd.read_sql_query(query, SQL_ENGINE)
    df = df.set_index("game_id")
    return df


if __name__ == "__main__":
    y = load_y()
