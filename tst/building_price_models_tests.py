import logging
import unittest

import os

from building_price_models import numpredict

class BuildingPriceModelTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def testWineprice(self):
        logging.info(numpredict.wineprice(95.0, 3.0))
        logging.info(numpredict.wineprice(95.0, 8.0))
        logging.info(numpredict.wineprice(99.0, 1.0))

        data = numpredict.wineset1()
        logging.info(data[0])
        logging.info(data[1])