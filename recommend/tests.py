import os
import unittest

import logging
from recommend.recommendations import critics, sim_distance, sim_pearson, topMatches, getRecommendations, transformPrefs


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
        self.assertEqual(0.15, r)

    def test_sim_pearson(self):
        r = sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
        self.assertEqual(0.4, r)

    def test_topMatches_with_sim_pearson_method(self):
        r = topMatches(critics, 'Toby', n=3)
        self.assertEqual(
            "[(0.99, 'Lisa Rose'), (0.92, 'Mick LaSalle'), (0.89, 'Claudia Puig')]",
            str(r))

    def test_getRecommendations_with_sim_pearson_method(self):
        pass
        r = getRecommendations(critics, 'Toby')
        self.assertEqual(
            "[(3.35, 'The Night Listener'), (2.83, 'Lady in the Water'), (2.53, 'Just My Luck')]",
            str(r))

    def test_getSimilarMovies(self):
        movies = transformPrefs(critics)
        r = topMatches(movies, 'Superman Returns')
        self.assertEqual(
            "[(0.66, 'You, Me and Dupree'), (0.49, 'Lady in the Water'), (0.11, 'Snakes on a Plane'), (-0.18, 'The Night Listener'), (-0.42, 'Just My Luck')]",
            str(r))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
