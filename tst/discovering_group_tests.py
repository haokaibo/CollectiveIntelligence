import os
import unittest

import logging

from discovering_group import clusters
from discovering_group.generatefeedvector import *


class GenerateFeedVectorTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data', 'blogdata')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def tearDown(self):
        pass

    def test_group_text_with_keywords(self):
        apcount = {}
        wordcounts = {}
        f = open(os.path.join(self.base_dir, 'feedlist.txt'))
        feedlist = [line for line in f]
        for feedurl in feedlist:
            try:
                title, wc = getwordcounts(feedurl)
                wordcounts[title] = wc
                for word, count in wc.items():
                    apcount.setdefault(word, 0)
                    if count > 1:
                        apcount[word] += 1
            except:
                print('Failed to parse feed %s' % feedurl)

        wordlist = []
        for w, bc in apcount.items():
            frac = float(bc) / len(feedlist)
            if frac > 0.1 and frac < 0.5:
                wordlist.append(w)

        output_path = os.path.join(self.base_dir, 'blogdata1.txt')
        out = open(output_path, 'w')
        out.write('Blog')
        for word in wordlist: out.write('\t%s' % word)
        out.write('\n')
        for blog, wc in wordcounts.items():
            logging.info(blog)
            out.write(blog)
            for word in wordlist:
                if word in wc:
                    out.write('\t%d' % wc[word])
                else:
                    out.write('\t0')
            out.write('\n')
        logging.info("Writing the blog data to %s." % output_path)

    def testHcluster(self):
        blog_data_file_path = os.path.join(self.base_dir, 'blogdata1.txt')
        blognames, words, data = clusters.readfile(blog_data_file_path)
        clust = clusters.hcluster(data)
        logging.info(clust)
        clusters.printclust(clust, labels=blognames)
        output_img_path =  os.path.join(self.base_dir, 'blogclust.jpg')
        clusters.drawdendrogram(clust, blognames, jpeg=output_img_path)


