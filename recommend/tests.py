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
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test')
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
        itemsim = calculateSimilarItems(critics)

        r = getRecommendedItems(critics, itemsim, 'Toby')
        self.assertEqual([(3.16, 'The Night Listener'), (2.61, 'Just My Luck'), (2.46, 'Lady in the Water')], r)

    def testLoadMovieLens(self):
        prefs = loadMovieLens(os.path.join(self.base_dir, 'movielens'))
        r = getRecommendations(prefs, '101')[0: 30]
        self.assertEqual(
            [(5.0, 'Zelary (2003)'), (5.0, 'World of Tomorrow (2015)'), (5.0, 'Woody Allen: A Documentary (2012)'),
             (5.0, 'Wish Upon a Star (1996)'), (5.0, 'War Room (2015)'), (5.0, 'Victoria (2015)'),
             (5.0, 'Unforgettable (1996)'), (5.0, 'Unfaithfully Yours (1948)'), (5.0, 'Undertow (2004)'),
             (5.0, 'Undefeated (2011)'), (5.0, 'Ugetsu (Ugetsu monogatari) (1953)'),
             (5.0, 'Trouble in Paradise (1932)'), (5.0, 'Trailer Park Boys (1999)'),
             (5.0, 'Through the Olive Trees (Zire darakhatan zeyton) (1994)'), (5.0, 'This Is the Army (1943)'),
             (5.0, 'The Slipper and the Rose: The Story of Cinderella (1976)'),
             (5.0, 'The Last Brickmaker in America (2001)'), (5.0, 'The Good Dinosaur (2015)'),
             (5.0, 'The Earrings of Madame de... (1953)'), (5.0, "Taste of Cherry (Ta'm e guilass) (1997)"),
             (5.0, 'Sympathy for Mr. Vengeance (Boksuneun naui geot) (2002)'), (5.0, 'Survive and Advance (2013)'),
             (5.0, 'Step Into Liquid (2002)'), (5.0, 'State of Siege (\xc3\x89tat de si\xc3\xa8ge) (1972)'),
             (5.0, 'Stargate: The Ark of Truth (2008)'), (5.0, 'Stargate: Continuum (2008)'),
             (5.0, 'Stalingrad (1993)'), (5.0, 'Sleepwalk with Me (2012)'), (5.0, 'Shogun Assassin (1980)'),
             (5.0, "Sgt. Pepper's Lonely Hearts Club Band (1978)")], r)


class PyDeliciousTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def tearDown(self):
        pass

    def test_get_popular(self):
        # r = pydelicious.get_popular(tag='programming')
        # logging.info(r)
        pass


if __name__ == '__main__':
    unittest.main(warnings='ignore')
