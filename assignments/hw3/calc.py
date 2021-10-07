"""Module calculates rolling batting averages
    from a 'master' list of stats per game.
"""

import sys

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


def calculate_ba(spark: SparkSession, mstr_df: DataFrame) -> DataFrame:
    # Emulate the rolling 100 days table.
    # since we have one table now, try out Spark SQL.
    # https://spark.apache.org/docs/2.2.0/sql-programming-guide.html
    mstr_df.createOrReplaceTempView("master")
    mstr_df.persist(StorageLevel.DISK_ONLY)
    rlng_df = spark.sql(ROLLING_SQL)
    return rlng_df


def main() -> int:
    return 0


if __name__ == "__main__":
    sys.exit(main())
