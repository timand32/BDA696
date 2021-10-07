"""Main app module for HW3.
"""
import sys

import calc
import data
from pyspark.sql import SparkSession


def main() -> int:
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    mstr_df = data.load_master_df(spark)
    rlng_df = calc.calculate_ba(spark, mstr_df)
    rlng_df.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
