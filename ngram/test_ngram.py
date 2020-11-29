"""
Tests for the NGramModel class
"""

from unittest import TestCase

from ngram import BEGIN_TOKEN, END_TOKEN, _count

class TestCount(TestCase):
    """
    Tests for `_count` function.
    """
    def setUp(self):
        self.simple_corpus = "I am Sam. Sam I am. I do not like green eggs and ham."

    def test_unigram(self, counts=None):
        """
        Test we get correct unigram counts on a simple corpus.
        """
        if not counts:
            counts = _count(self.simple_corpus, 1)
            self.assertEqual(len(counts), 1)
        unigrams = counts[0]
        self.assertEqual(len(unigrams), 12)
        expected_grams = {("I",), ("am",), ("Sam",), (".",), (END_TOKEN,), ("do",), ("not",),
                          ("like",), ("green",), ("eggs",), ("and",), ("ham",)}
        self.assertEqual(set(unigrams.keys()), expected_grams)
        for gram in expected_grams:
            count = unigrams[gram]
            if gram in [("I",), (".",), (END_TOKEN,)]:
                self.assertEqual(count, 3)
            elif gram in [("am",), ("Sam",)]:
                self.assertEqual(count, 2)
            else:
                self.assertEqual(count, 1)

    def test_bigram(self, counts=None):
        """
        Test we get correct bigram and unigram counts on a simple corpus.
        """
        if not counts:
            counts = _count(self.simple_corpus, 2)
            self.assertEqual(len(counts), 2)
        bigrams = counts[1]
        self.assertEqual(len(bigrams), 16)
        expected_grams = {(BEGIN_TOKEN, "I"), ("I", "am"), ("am", "Sam"), ("Sam", "."),
                          (".", END_TOKEN), (BEGIN_TOKEN, "Sam"), ("Sam", "I"), ("am", "."),
                          ("I", "do"), ("do", "not"), ("not", "like"), ("like", "green"),
                          ("green", "eggs"), ("eggs", "and"), ("and", "ham"), ("ham", ".")}
        self.assertEqual(set(bigrams.keys()), expected_grams)
        for gram in expected_grams:
            count = bigrams[gram]
            if gram == (".", END_TOKEN):
                self.assertEqual(count, 3)
            elif gram in [(BEGIN_TOKEN, "I"), ("I", "am")]:
                self.assertEqual(count, 2)
            else:
                self.assertEqual(count, 1)
        self.test_unigram(counts)

    def test_trigram(self):
        """
        Test we get correct trigram, bigram and unigram counts on a simple corpus.
        """
        counts = _count(self.simple_corpus, 3)
        self.assertEqual(len(counts), 3)
        trigrams = counts[2]
        self.assertEqual(len(trigrams), 17)
        expected_grams = {(BEGIN_TOKEN, "I", "am"), ("I", "am", "Sam"), ("am", "Sam", "."),
                          ("Sam", ".", END_TOKEN), (BEGIN_TOKEN, "Sam", "I"), ("Sam", "I", "am"),
                          ("I", "am", "."), ("am", ".", END_TOKEN), (BEGIN_TOKEN, "I", "do"),
                          ("I", "do", "not"), ("do", "not", "like"), ("not", "like", "green"),
                          ("like", "green", "eggs"), ("green", "eggs", "and"),
                          ("eggs", "and", "ham"), ("and", "ham", "."), ("ham", ".", END_TOKEN)}
        self.assertEqual(set(trigrams.keys()), expected_grams)
        for gram in expected_grams:
            count = trigrams[gram]
            self.assertEqual(count, 1)
        self.test_bigram(counts)
