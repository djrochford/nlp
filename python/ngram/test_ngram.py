"""
Tests for the NGramModel class
"""

from unittest import TestCase

from ngram import BEGIN_TOKEN, END_TOKEN, _calculate_probabilities, _count

SIMPLE_CORPUS = "I am Sam. Sam I am. I do not like green eggs and ham."

class TestCount(TestCase):
    """
    Tests for `_count` function.
    """

    def test_unigram(self, counts=None):
        """
        Test we get correct unigram counts on a simple corpus.
        """
        if not counts:
            counts = _count(SIMPLE_CORPUS, 1)
            self.assertEqual(len(counts), 1)
        unigrams = counts[0]
        self.assertEqual(len(unigrams), 13)
        expected_grams = {(BEGIN_TOKEN,), ("I",), ("am",), ("Sam",), (".",), (END_TOKEN,), ("do",),
                          ("not",), ("like",), ("green",), ("eggs",), ("and",), ("ham",)}
        self.assertEqual(set(unigrams.keys()), expected_grams)
        for gram in expected_grams:
            count = unigrams[gram]
            if gram in [(BEGIN_TOKEN,), ("I",), (".",), (END_TOKEN,)]:
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
            counts = _count(SIMPLE_CORPUS, 2)
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
        counts = _count(SIMPLE_CORPUS, 3)
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

class TestCalcProb(TestCase):
    """
    Tests for `_calculate_probabilities` function.
    """

    def test_unigram(self, probs=None):
        """
        Test we get accurate (asbolute) probabilities of unigrams of simple corpus.
        """
        if not probs:
            probs = _calculate_probabilities(_count(SIMPLE_CORPUS, 1))
            self.assertEqual(len(probs), 1)
        unigram_probs = probs[0]
        self.assertEqual(len(unigram_probs), 13)
        expected_grams = {(BEGIN_TOKEN,), ("I",), ("am",), ("Sam",), (".",), (END_TOKEN,), ("do",), ("not",),
                          ("like",), ("green",), ("eggs",), ("and",), ("ham",)}
        self.assertEqual(set(unigram_probs.keys()), expected_grams)
        for gram in expected_grams:
            prob = unigram_probs[gram]
            if gram in [(BEGIN_TOKEN,), ("I",), (".",), (END_TOKEN,)]:
                self.assertEqual(prob, 3/23)
            elif gram in [("am",), ("Sam",)]:
                self.assertEqual(prob, 2/23)
            else:
                self.assertEqual(prob, 1/23)

    def test_bigram(self, probs=None):
        """
        Test we get correct (conditional) bigram and (absolute) unigram probabilities on a simple corpus.
        """
        if not probs:
            probs = _calculate_probabilities(_count(SIMPLE_CORPUS, 2))
            self.assertEqual(len(probs), 2)
        bigram_probs = probs[1]
        self.assertEqual(len(bigram_probs), 16)
        expected_grams = {(BEGIN_TOKEN, "I"), ("I", "am"), ("am", "Sam"), ("Sam", "."),
                          (".", END_TOKEN), (BEGIN_TOKEN, "Sam"), ("Sam", "I"), ("am", "."),
                          ("I", "do"), ("do", "not"), ("not", "like"), ("like", "green"),
                          ("green", "eggs"), ("eggs", "and"), ("and", "ham"), ("ham", ".")}
        self.assertEqual(set(bigram_probs.keys()), expected_grams)
        for gram in expected_grams:
            prob = bigram_probs[gram]
            if gram in [(BEGIN_TOKEN, "I"), ("I", "am")]:
                self.assertEqual(prob, 2/3)
            elif gram in [("am", "Sam"), ("Sam", "."), ("Sam", "I"), ("am", ".")]:
                self.assertEqual(prob, 1/2)
            elif gram in [(BEGIN_TOKEN, "Sam"), ("I", "do")]:
                self.assertEqual(prob, 1/3)
            else:
                self.assertEqual(prob, 1)
        self.test_unigram(probs)

    def test_trigram(self, probs=None):
        """
        Test we get correct (conditional) bigram and (absolute) unigram probabilities on a simple corpus.
        """
        if not probs:
            probs = _calculate_probabilities(_count(SIMPLE_CORPUS, 3))
            self.assertEqual(len(probs), 3)
        trigram_probs = probs[2]
        self.assertEqual(len(trigram_probs), 17)
        expected_grams = {(BEGIN_TOKEN, "I", "am"), ("I", "am", "Sam"), ("am", "Sam", "."),
                          ("Sam", ".", END_TOKEN), (BEGIN_TOKEN, "Sam", "I"), ("Sam", "I", "am"),
                          ("I", "am", "."), ("am", ".", END_TOKEN), (BEGIN_TOKEN, "I", "do"),
                          ("I", "do", "not"), ("do", "not", "like"), ("not", "like", "green"),
                          ("like", "green", "eggs"), ("green", "eggs", "and"),
                          ("eggs", "and", "ham"), ("and", "ham", "."), ("ham", ".", END_TOKEN)}
        self.assertEqual(set(trigram_probs.keys()), expected_grams)
        for gram in expected_grams:
            prob = trigram_probs[gram]
            if gram in [(BEGIN_TOKEN, "I", "am"), ("I", "am", "Sam"), ("I", "am", "."),
                        (BEGIN_TOKEN, "I", "do")]:
                self.assertEqual(prob, 1/2)
            else:
                self.assertEqual(prob, 1)
        self.test_bigram(probs)
