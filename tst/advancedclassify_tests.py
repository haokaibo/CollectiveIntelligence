import logging
import os
import unittest
from advancedclassify import *


class AdvancedClassifyTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data', 'matchmaker')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def test_load_data(self):
        agesonly = loadmatch(os.path.join(self.base_dir, 'agesonly.csv'), allnum=True)
        matchmaker = loadmatch(os.path.join(self.base_dir, 'matchmaker.csv'))
        plot_age_matches(agesonly)