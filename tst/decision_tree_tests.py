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

    def testGiniimpurity(self):
        logging.info(giniimpurity(my_data))

    def testEntropy(self):
        logging.info(entropy(my_data))

    def testDivideSet2(self):
        set1, set2 = DecisionTree.divideset(my_data, 2, 'yes')
        logging.info("Entorpy of set1: %s" % DecisionTree.entropy(set1))
        logging.info("Ginimpurity of set1: %s" % DecisionTree.giniimpurity(set1))

    def testBuildTree(self):
        tree = buildtree(my_data)
        DecisionTree.printtree(tree)

    def testDrawTree(self):
        tree = buildtree(my_data)
        DecisionTree.drawtree(tree, jpeg='treeview.jpg')



if __name__ == '__main__':
    unittest.main(warnings='ignore')
