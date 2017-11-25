import os
import unittest

import logging

from decision_tree.treepredict import *


class DecisionTreeTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def tearDown(self):
        pass

    def testDivideSet(self):
        logging.info(DecisionTree.divideset(my_data, 2, 'yes'))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
