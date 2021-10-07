"""Module defines custom RDD transformers.
"""

import calc
from pyspark import keyword_only
from pyspark.ml import Transformer
from pyspark.sql import SparkSession


class RollingBATransform(Transformer):
    """A pyspark Transformer for calculating rolling BA averages.

    Takes no additional parameters.
    """

    @keyword_only
    def __init__(self):
        super(RollingBATransform, self).__init__()
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    @keyword_only
    def setParams(self):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def _transform(self, dataset):
        # Stack overflow Q# 56190852:
        # I can grab the active spark session here
        spark = SparkSession.builder.getOrCreate()
        dataset = calc.calculate_ba(spark, dataset)
        return dataset
