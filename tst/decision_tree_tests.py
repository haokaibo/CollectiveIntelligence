import csv
import os
import unittest

import logging

from decision_tree.treepredict import *
from decision_tree.zillow import *
from decision_tree.hotornot import *

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
        logging.info("Entorpy of set1: %s" % entropy(set1))
        logging.info("Ginimpurity of set1: %s" % giniimpurity(set1))

    def testBuildTree(self):
        tree = buildtree(my_data)
        DecisionTree.printtree(tree)

    def testDrawTree(self):
        tree = buildtree(my_data)
        DecisionTree.drawtree(tree, jpeg='treeview.jpg')

    def testClassify(self):
        tree = buildtree(my_data)
        r = classify(['(direct)', 'USA', 'yes', 5], tree)
        logging.info(r)

    def testPrune(self):
        tree = buildtree(my_data)
        prune(tree, 0.1)
        DecisionTree.printtree(tree)

        prune(tree, 1.0)
        DecisionTree.printtree(tree)

    def testMdclassify(self):
        tree = buildtree(my_data)
        r = mdclassify(['google', None, 'yes', None], tree)
        logging.info(r)
        r = mdclassify(['google', 'France', None, None], tree)
        logging.info(r)

    def testGetpricelist(self):
        zillow_path = os.path.join(self.base_dir, 'zillow')
        housedata = getpricelist(os.path.join(zillow_path, 'addresslist.txt'))
        valid_housedata = [row for row in housedata if row is not None]
        # housedata_filepath = os.path.join(zillow_path, 'housedata.csv')
        # housedata_file = open(housedata_filepath, 'w')
        # wr = csv.writer(housedata_file)
        housetree = buildtree(valid_housedata, scoref=variance)
        DecisionTree.drawtree(housetree, os.path.join(zillow_path, 'housetree.jpg'))

    def testHotornot(self):
        l1 = getrandomratings(500)
        len(l1)

        pdata = getpeopledata(l1)
        logging.info(pdata[0])

        hottree = buildtree(pdata, scoref=variance)
        prune(hottree)
        DecisionTree.drawtree(hottree, os.path.join((self.base_dir, 'hotornot', 'hosttree.jpg')))

if __name__ == '__main__':
    unittest.main(warnings='ignore')
