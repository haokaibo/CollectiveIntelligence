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




if __name__ == '__main__':
    unittest.main(warnings='ignore')
