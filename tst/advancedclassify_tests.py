import logging
import json
import os
import unittest
from advancedclassify import *
from csv import writer


class AdvancedClassifyTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data', 'matchmaker')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        with open(os.path.join(self.base_dir, 'bing_conf'), 'r') as config_file:
            content = config_file.read()
        self.bing_map_key = json.loads(content)['bing_map_key']

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
        logging.info(getlocation('1 alewife center, cambridge, ma', self.bing_map_key))

    def test_milesdistance(self):
        logging.info(milesdistance('cambridge, ma', 'new york,ny', self.bing_map_key))

    def test_loadnumerical(self):
        newrows = loadnumerical(os.path.join(self.base_dir, 'matchmaker.csv'), self.bing_map_key)

        numerical_matchmaker_file_path = os.path.join(self.base_dir, 'numerical_matchmaker.csv')

        with open(numerical_matchmaker_file_path, 'w') as num_file:
            file_writer = writer(num_file)
            for row in newrows:
                try:
                    file_writer.writerow(row.data + [row.match])
                except Exception:
                    print('str_row_data=%s', row.data)
