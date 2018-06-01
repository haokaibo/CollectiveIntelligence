import logging
import json
import os
import unittest
from collections import namedtuple

from advancedclassify import *
from csv import writer, reader


class AdvancedClassifyTest(unittest.TestCase):
    def setUp(self):
        a = namedtuple('a', [])
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
            csv_writer = writer(num_file)
            for row in newrows:
                try:
                    csv_writer.writerow(row.data + [row.match])
                except Exception:
                    print('str_row_data=%s', row.data)

    def test_scaledata(self):
        numerical_matchmaker_file_path = os.path.join(self.base_dir, 'numerical_matchmaker.csv')
        with open(numerical_matchmaker_file_path, 'r') as num_file:
            csv_reader = reader(num_file)
            num_rows = []
            for row in csv_reader:
                match_row = matchrow(map(float, row))
                num_rows.append(match_row)

        if len(num_rows) > 0:
            scaled_rows, scaleinput = scaledata(num_rows)
            scaled_matchmaker_file_path = os.path.join(self.base_dir, 'scaled_matchmaker.csv')
            with open(scaled_matchmaker_file_path, 'w') as scaled_file:
                csv_writer = writer(scaled_file)
                for row in scaled_rows:
                    try:
                        csv_writer.writerow(row.data + [row.match])
                    except Exception:
                        print('str_scaled_row_data=%s', row.data)

    def test_classify_by_scaled_data(self):
        # load high and low from the numerical data
        numerical_matchmaker_file_path = os.path.join(self.base_dir, 'numerical_matchmaker.csv')
        # low = [999999999.0] * 7
        # high = [-999999999.0] * 7

        numerical_rows = []
        with open(numerical_matchmaker_file_path) as numerical_file:
            csv_reader = reader(numerical_file)
            for row in csv_reader:
                row = map(float, row)
                numerical_rows.append(matchrow(map(float, row)))
                # for i in range(len(row) - 1):
                #     if row[i] < low[i]: low[i] = row[i]
                #     if row[i] > high[i]: high[i] = row[i]

        scaledset, scalef = scaledata(numerical_rows)
        avgs = lineartrain(scaledset)

        print(numerical_rows[0].data)
        print('match=%s' % numerical_rows[0].match)
        scalefed = scalef(numerical_rows[0])
        print(dpclassify(scalefed[0: len(scalefed) - 1], avgs))

        print(numerical_rows[11].data)
        print('match=%s' % numerical_rows[11].match)
        scalefed = scalef(numerical_rows[11])
        print(dpclassify(scalefed[0: len(scalefed) - 1], avgs))
