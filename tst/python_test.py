import os
import unittest

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging

from recommend.recommendations import *


class PandasTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def tearDown(self):
        pass

    def test_dataframe(self):
        s = pd.Series([1, 3, 5, np.nan, 6, 8])
        logging.info(s)

        dates = pd.date_range('20130101', periods=6)

        logging.info(dates)

        df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))

        logging.info(df)

        df2 = pd.DataFrame({'A': 1.,
                            'B': pd.Timestamp('20130102'),
                            'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                            'D': np.array([3] * 4, dtype='int32'),
                            'E': pd.Categorical(['test', 'train', 'test', 'train']),
                            'F': 'foo'})
        logging.info(df2)

        logging.info(df2.dtypes)

        logging.info(df.head())

        logging.info(df.tails(3))

        logging.info(df.index)

        logging.info(df.columns)

        logging.info(df.values)

        logging.info(df.describe())


if __name__ == '__main__':
    unittest.main(warnings='ignore')
