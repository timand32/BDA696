"""Module loads dataset into spark DataFrames from MariaDB.
"""
import sys

from pyspark.sql import DataFrame, SparkSession

JDBC_NAME = "mysql"
"""Perhaps this was suppose to be 'mariadb',
but I got an error whenever I used .show()
(Same problem as Stack Exchange Q. 56019251)
"""

DB_SERVER_URL = "localhost:3306"
DB_NAME = "baseball"
DB_USERNAME = "root"
DB_PASSWORD = "password"


def _read_table(spark: SparkSession, table_name: str) -> DataFrame:
    """Load a table with a given spark session.

    Note this is a private module function.
    It is not intended to be used outside of the module.
    """
    # Code heavily adapted from Spark's python documentation.
    return spark.read.jdbc(
        f"jdbc:{JDBC_NAME}://{DB_SERVER_URL}/{DB_NAME}",
        table_name,
        properties={"user": DB_USERNAME, "password": DB_PASSWORD},
    )


def load_master_df(spark: SparkSession) -> DataFrame:
    # Emulate the 'master' table from the SQL example
    # using DataFrame methods.
    # Read batter_counts table from active MariaDB database.
    # Also emulate the select and where clauses
    bc_df = _read_table(spark, "batter_counts")
    bc_df = bc_df.select("game_id", "batter", "atBat", "Hit")
    bc_df = bc_df.where(bc_df["Hit"] > 0)
    # Do the same for the game table.
    g_df = _read_table(spark, "game")
    g_df = g_df.select("game_id", "local_date")
    # Emulate the join
    mstr_df = bc_df.join(g_df, "game_id")
    return mstr_df


def main() -> int:
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    mstr_df = load_master_df(spark)
    mstr_df.show(n=5)
    return 0


if __name__ == "__main__":
    sys.exit(main())
