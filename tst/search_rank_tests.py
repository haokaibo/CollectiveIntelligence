import logging
import os
import unittest

from search_rank import searchengine


class RecommendationsTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data')
        self.test_db_path = '/Users/kaibohao/Documents/Kaibo/CapacityPlanning/src/CollectiveIntelligence/search_rank/searchindex.db'
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def tearDown(self):
        pass

    def test_crawl(self):
        crawler = searchengine.crawler(self.test_db_path)
        pages = ['http://en.wikipedia.org/wiki/Kindle']
        crawler.crawl(pages)

    def test_getmatchrows(self):
        searcher = searchengine.searcher(self.test_db_path)
        r = searcher.getmatchrows('Amazon Kindle')
