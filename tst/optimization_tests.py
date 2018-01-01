import unittest

import os

import optimization
import logging

from optimization import dorm
from optimization.dorm import printsolution, domain, dormcost
from optimization.optimization import *


class OptimizationTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        load_data_from_file(os.path.join(self.base_dir, 'optimization', 'schedule.txt'))

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
        domain = [(0, 8)] * (len(people) * 2)
        s = randomoptimize(domain, schedulecost)
        logging.info(schedulecost(s))
        printschedule(s)

    def testHillclimb(self):
        domain = [(0, 8)] * (len(people) * 2)
        s = hillclimb(domain, schedulecost)
        logging.info(schedulecost(s))
        printschedule(s)

    def testAnnealingoptimize(self):
        domain = [(0, 8)] * (len(people) * 2)
        s = annealingoptimize(domain, schedulecost)
        logging.info("cost=%d", schedulecost(s))
        printschedule(s)

    def testGeneticoptimize(self):
        domain = [(0, 8)] * (len(people) * 2)
        s = geneticoptimize(domain, schedulecost)
        printschedule(s)

    # ### dorm test ###

    def testPrintSolution(self):
        printsolution([0,0,0,0,0,0,0,0,0,0])

    def testDormcost(self):
        s= randomoptimize(domain, dormcost)
        dormcost(s)
        printschedule(s)

        s= geneticoptimize(domain, dormcost)
        printsolution(s)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
