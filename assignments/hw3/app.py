"""Main app module for HW3.
"""
import sys

# import calc
import data
from pyspark.sql import SparkSession
from transformers import RollingBATransform


def main() -> int:
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    mstr_df = data.load_master_df(spark)
    # rlng_df = calc.calculate_ba(spark, mstr_df)
    transformer = RollingBATransform()
    rlng_df = transformer.transform(mstr_df, {})
    rlng_df.show(n=5)
    return 0


if __name__ == "__main__":
    sys.exit(main())
