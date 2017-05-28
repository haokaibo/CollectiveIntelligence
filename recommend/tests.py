import os
import unittest

import logging

import recommend
from recommend import recommendations
from recommend.recommendations import *

import pydelicious


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

    def testCalculateSimilarItems(self):
        reload(recommendations)
        itemsim = calculateSimilarItems(critics)
        self.assertEqual(
            {'Lady in the Water': [(0.4, 'You, Me and Dupree'), (0.29, 'The Night Listener'),
                                   (0.22, 'Snakes on a Plane'), (0.22, 'Just My Luck'), (0.09, 'Superman Returns')],
             'Snakes on a Plane': [(0.22, 'Lady in the Water'), (0.18, 'The Night Listener'),
                                   (0.17, 'Superman Returns'), (0.11, 'Just My Luck'), (0.05, 'You, Me and Dupree')],
             'Just My Luck': [(0.22, 'Lady in the Water'), (0.18, 'You, Me and Dupree'), (0.15, 'The Night Listener'),
                              (0.11, 'Snakes on a Plane'), (0.06, 'Superman Returns')],
             'Superman Returns': [(0.17, 'Snakes on a Plane'), (0.1, 'The Night Listener'), (0.09, 'Lady in the Water'),
                                  (0.06, 'Just My Luck'), (0.05, 'You, Me and Dupree')],
             'You, Me and Dupree': [(0.4, 'Lady in the Water'), (0.18, 'Just My Luck'), (0.15, 'The Night Listener'),
                                    (0.05, 'Superman Returns'), (0.05, 'Snakes on a Plane')],
             'The Night Listener': [(0.29, 'Lady in the Water'), (0.18, 'Snakes on a Plane'),
                                    (0.15, 'You, Me and Dupree'), (0.15, 'Just My Luck'), (0.1, 'Superman Returns')]},
            itemsim)

    def testgetRecommendedItems(self):
        reload(recommendations)
        itemsim = calculateSimilarItems(critics)

        reload(recommendations)
        r = getRecommendedItems(critics, itemsim, 'Toby')
        self.assertEqual([(3.16, 'The Night Listener'), (2.61, 'Just My Luck'), (2.46, 'Lady in the Water')], r)


class PyDeliciousTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def tearDown(self):
        pass

    def test_get_popular(self):
        r = pydelicious.get_popular(tag='programming')
        logging.info(r)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
