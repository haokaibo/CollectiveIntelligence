import os
import unittest

import logging
from recommend.recommendations import critics, sim_distance, sim_pearson, topMatches


class RecommendationsTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def tearDown(self):
        pass

    def test_sim_distance(self):
        r = sim_distance(critics, 'Lisa Rose', 'Gene Seymour')
        self.assertEqual(0.14814814814814814, r)

    def test_sim_pearson(self):
        r = sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
        self.assertEqual(0.39605901719066977, r)

    def test_topMatches_with_sim_pearson_method(self):
        r = topMatches(critics, 'Toby', n=3)
        self.assertEqual(
            "[(0.9912407071619299, 'Lisa Rose'), (0.9244734516419049, 'Mick LaSalle'), (0.8934051474415647, 'Claudia Puig')]",
            str(r))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
