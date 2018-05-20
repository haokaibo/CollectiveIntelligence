import logging
import json
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
        print('OK')

    def test_lineartrain(self):
        agesonly = loadmatch(os.path.join(self.base_dir, 'agesonly.csv'), allnum=True)
        r = lineartrain(agesonly)
        logging.info(r)

    def test_dpclassify(self):
        agesonly = loadmatch(os.path.join(self.base_dir, 'agesonly.csv'), allnum=True)
        avgs = lineartrain(agesonly)
        logging.info(dpclassify([30, 30], avgs))
        logging.info(dpclassify([30, 25], avgs))
        logging.info(dpclassify([25, 40], avgs))
        logging.info(dpclassify([48, 20], avgs))

    def test_getlocation(self):
        file = open(os.path.join(self.base_dir, 'bing_conf'))
        content = file.read()
        bing_map_key = json.loads(content)['bing_map_key']
        logging.info(getlocation('1 alewife center, cambridge, ma', bing_map_key))

    def test_milesdistance(self):
        logging.info(milesdistance('cambridge, ma', 'new york,ny'))

    def loadnumerical(self):
        oldrows = loadmatch(os.path.join(self.base_dir, 'matchmaker.csv'))

        newrows = []
        for row in oldrows:
            d = row.data
            data = [float(d[0]), yesno(d[1]), yesno(d[2]),
                    float(d[5]), yesno(d[6]), yesno(d[7]),
                    matchcount(d[3], d[8]),
                    milesdistance(d[4], d[9]),
                    row.match]
            newrows.append(matchrow(data))
        return newrows

