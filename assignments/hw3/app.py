"""Main app module for HW3.
"""
import sys

import data
from pyspark.sql import SparkSession
from transformers import RollingBATransform


def main() -> int:
    # Builda a Spark session
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    # Load and process a 'master' DF of stats per batter per game
    mstr_df = data.load_master_df(spark)
    print(f"Loaded, selected, and joined DF:\n{30*'='}")
    mstr_df.show()
    # Transform a master DF into a DF of rolling averages.
    transformer = RollingBATransform()
    rlng_df = transformer.transform(mstr_df, {})
    print(f"Transformed DF:\n{20*'='}")
    rlng_df.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
