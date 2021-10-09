"""Module calculates rolling batting averages
    from a 'master' list of stats per game.
"""

from pyspark import StorageLevel
from pyspark.sql import DataFrame, SparkSession

ROLLING_SQL = """
SELECT
    m1.batter,
    m1.game_id,
    m1.local_date,
    SUM(m2.Hit) / SUM(m2.atBat) AS ba
FROM
    master m1
JOIN master m2
    ON m1.batter = m2.batter
    AND m2.local_date
        BETWEEN DATE_SUB(m1.local_date, 100)
        AND m1.local_date
GROUP BY m1.batter, m1.game_id, m1.local_date
SORT BY m1.batter, m1.game_id, m1.local_date;
"""
"""Query calculates rolling SQL average
given a master list of hits and at bats
per batter, per game/date.

Adapted from professor's mysql (@dafrenchyman's) example.
"""


def calculate_ba(spark: SparkSession, mstr_df: DataFrame) -> DataFrame:
    """Calculates 100-day rolling batting average
    from a master list of stats per batter per game.

    Args:
        spark (SparkSession): A spark jdbf session.
        mstr_df (DataFrame): A DataFrame of stats
        per batter per game.

    Returns:
        DataFrame: A DataFrame of rolling BA per game.
    """
    # Emulate the rolling 100 days table.
    # since we have one table now, try out Spark SQL.
    # https://spark.apache.org/docs/2.2.0/sql-programming-guide.html
    mstr_df.createOrReplaceTempView("master")
    mstr_df.persist(StorageLevel.DISK_ONLY)
    rlng_df = spark.sql(ROLLING_SQL)
    return rlng_df
