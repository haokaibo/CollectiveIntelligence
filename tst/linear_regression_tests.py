import os
import unittest

import numpy as np
import matplotlib.pyplot as plt
import logging

from recommend.recommendations import *


class PandasTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data', 'linear_regression')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def tearDown(self):
        pass

    def test_multiple_variables(self):
        X= np.loadtxt(os.path.join(self.base_dir, 'data.txt'), delimiter=',', usecols=(0, 1), unpack=True,
                          dtype=int)
        y = np.loadtxt(os.path.join(self.base_dir, 'data.txt'), delimiter=',', usecols=(2), unpack=True,
                       dtype=int)
        print(X)
        print(y)

        m = len(y)
        print(m)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
