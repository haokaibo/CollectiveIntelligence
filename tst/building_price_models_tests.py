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

    def testEuclidean(self):
        data = numpredict.wineset1()
        data0 = data[0]
        data1 = data[1]
        logging.info('data0: %s', data0)
        logging.info('data1: %s', data1)

        logging.info(numpredict.euclidean(data0['input'], data1['input']))

    def testKnnestimate(self):
        data = numpredict.wineset1()
        logging.info(numpredict.knnestimate(data, (95.0, 3.0)))
        logging.info(numpredict.knnestimate(data, (99.0, 3.0)))
        logging.info(numpredict.knnestimate(data, (99.0, 5.0)))
        logging.info(numpredict.wineprice(99.0, 5.0))
        logging.info(numpredict.knnestimate(data, (95.0, 3.0), k=1))

    def testSubstractweight(self):
        logging.info(numpredict.substractweight(0.1))
        logging.info(numpredict.substractweight(1))

    def testInverseweight(self):
        logging.info(numpredict.inverseweight(0.1))
        logging.info(numpredict.inverseweight(1))

    def testGaussian(self):
        logging.info(numpredict.gaussian(0.1))
        logging.info(numpredict.gaussian(1.0))
        logging.info(numpredict.gaussian(3.0))

    def testWeightedknn(self):
        data = numpredict.wineset1()
        logging.info(numpredict.weightedknn(data, (99.5, 5.0)))

    def testCrossvalidate(self):
        data = numpredict.wineset1()
        logging.info("kn3=%f" % numpredict.crossvalidate(numpredict.knnestimate, data))

        def knn5(d, v): return numpredict.knnestimate(d, v, k=5)

        logging.info("kn5=%f" % numpredict.crossvalidate(knn5, data))

        def knn1(d, v): return numpredict.knnestimate(d, v, k=1)

        logging.info("kn1=%f" % numpredict.crossvalidate(knn1, data))

        def knn10(d, v): return numpredict.knnestimate(d, v, k=10)

        logging.info("kn10=%f" % numpredict.crossvalidate(knn10, data))

        logging.info("weightedknn=%f" % numpredict.crossvalidate(numpredict.weightedknn, data))

        def knniverse(d, v):
            return numpredict.weightedknn(d, v, weightf=numpredict.inverseweight)

        logging.info("knninverse=%f", numpredict.crossvalidate(knniverse, data))

    def testCrossvalidate_with_wineset2(self):
        data = numpredict.wineset2()
        logging.info("knn3=%f" % numpredict.crossvalidate(numpredict.knnestimate, data))
        logging.info("weightedknn=%f" % numpredict.crossvalidate(numpredict.weightedknn, data))

    def testRescale(self):
        data = numpredict.wineset2()
        sdata = numpredict.rescale(data, [10, 10, 0, 0.5])
        logging.info("knn3=%f" % numpredict.crossvalidate(numpredict.knnestimate, sdata))
        logging.info("weightedknn=%f" % numpredict.crossvalidate(numpredict.weightedknn, sdata))

    def testWineset3(self):
        data = numpredict.wineset3()
        logging.info("wine price=%f" % numpredict.wineprice(99.0, 20.0))
        logging.info("weightedknn=%f" % numpredict.weightedknn(data, [99.0, 20.0]))
        logging.info("crossvalidate=%f" % numpredict.crossvalidate(numpredict.weightedknn, data))

    def testProbguess(self):
        data = numpredict.wineset3()
        ranges = [[40, 80], [80, 120], [120, 1000], [30, 120]]
        for r in ranges:
            logging.info(
                "Probability in %d to %d is %f" % (r[0], r[1], numpredict.probguess(data, [99, 20], r[0], r[1])))

    def testCumulativegrph(self):
        data = numpredict.wineset3()
        numpredict.cumulativegraph(data, (1, 1), 60)
