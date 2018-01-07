import unittest

import os

import optimization
import logging

from optimization import dorm, socialnetwork
from optimization.dorm import printsolution, domain, dormcost
from optimization.optimization import *
from optimization.socialnetwork import drawnetwork


class OptimizationTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        load_data_from_file(os.path.join(self.base_dir, 'optimization', 'schedule.txt'))
        domain = [(0, 8)] * (len(people) * 2)

    def tearDown(self):
        pass

    def testPrintfschedule(self):
        s = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
        printschedule(s)

    def testSchedulecost(self):
        s = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
        cost = schedulecost(s)
        logging.info("cost=%d" % cost)

    def testRandomoptimize(self):
        s = randomoptimize(domain, schedulecost)
        logging.info(schedulecost(s))
        printschedule(s)

    def testHillclimb(self):
        s = hillclimb(domain, schedulecost)
        logging.info(schedulecost(s))
        printschedule(s)

    def testAnnealingoptimize(self):
        s = annealingoptimize(domain, schedulecost)
        logging.info("cost=%d", schedulecost(s))
        printschedule(s)

    def testGeneticoptimize(self):
        s = geneticoptimize(domain, schedulecost)
        printschedule(s)


class DormTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def tearDown(self):
        pass

    # ### dorm test ###

    def testPrintSolution(self):
        printsolution([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def testDormcost(self):
        s = randomoptimize(dorm.domain, dormcost)
        logging.info("s=%s" % s)
        logging.info('dorm cost=%d' % dormcost(s))
        printsolution(s)

        # s = geneticoptimize(dorm.domain, dormcost)
        # printsolution(s)


class SocialnetworkTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def tearDown(self):
        pass

    def testSocialNetwork(self):
        sol = randomoptimize(socialnetwork.domain, socialnetwork.crosscount, times=1)
        logging.info('randomoptimize cost = %d' % socialnetwork.crosscount(sol))

        sol = annealingoptimize(socialnetwork.domain, socialnetwork.crosscount, step=50, cool=0.99)
        logging.info('annealingoptimize cost = %d' % socialnetwork.crosscount(sol))

        logging.info('sol=%s' % sol)

    def testDrawngitetwork(self):
        sol = randomoptimize(socialnetwork.domain, socialnetwork.crosscount, times=1000)
        logging.info('annealingoptimize cost = %d' % socialnetwork.crosscount(sol))
        logging.info('sol=%s' % sol)
        drawnetwork(sol)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
