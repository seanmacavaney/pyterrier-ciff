import random
import tempfile
import unittest
import pyterrier_ciff
import pandas as pd
import string

from pyterrier_ciff import CiffIndex, PostingsList, DocRecord

TOKS = string.ascii_letters + string.digits

def _rand_toks():
    toks = random.sample(TOKS, random.randrange(len(TOKS)))
    return {t: random.gauss(mu=1., sigma=1.) for t in toks}


class TestIndexer(unittest.TestCase):
    def test_index(self):
        with tempfile.TemporaryDirectory() as d:
            with self.subTest('index init'):
                index = CiffIndex(f'{d}/test.ciff')
                self.assertFalse(index.built())

            with self.subTest('indexing'):
                indexer = index.indexer()
                num_docs = random.randrange(10_000, 100_000)
                inp = ({'docno': str(i), 'toks': _rand_toks()} for i in range(num_docs))
                res = indexer.index(inp)
                self.assertTrue(index.built())
                self.assertEqual(res, index)

            with self.subTest('header'):
                header = index.header()
                self.assertEqual(header.version, 1)
                self.assertEqual(header.num_docs, num_docs)
                self.assertEqual(header.total_docs, num_docs)
                self.assertEqual(header.description, "pyterrier-ciff")

            with self.subTest('posting lists and doc records'):
                count_postings_lists = 0
                count_docs = 0
                cf = 0
                for record in index:
                    if isinstance(record, PostingsList):
                        count_postings_lists += 1
                        for posting in record.postings:
                            cf += posting.tf
                    if isinstance(record, DocRecord):
                        count_docs += 1
                # self.assertEqual(count_docs, num_docs)
                self.assertEqual(count_postings_lists, header.num_postings_lists)
