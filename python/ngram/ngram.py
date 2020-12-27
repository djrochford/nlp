"""
Ngram language model class and functions that operate on it.
"""
import re
from collections import defaultdict
from typing import DefaultDict, List, Tuple

from nltk import sent_tokenize, word_tokenize # type: ignore

CountObject = List[DefaultDict[Tuple[str, ...], int]]
NgramContainer = List[DefaultDict[Tuple[str, ...], float]]

class NgramModel:
    """
    Ngram language model.
    """

    def __init__(self, training_text: str, order: int):
        self._ngrams = _calculate_probabilities(_count(training_text, order))
        self._order = order

    def __getitem__(self, key):
        if key < 0:
            raise IndexError("Cannot index NgramModel instance with negative numbers")
        return self._ngrams[key - 1]

    @property
    def ngrams(self) -> NgramContainer:
        """
        The items in the `_ngrams` list are dicts from ngrams to probabilities. (Absolute
        probabilities in the case of unigrams, conditional otherwise.) The firt dict in the list has
        unigram keys, the second bigram, and so on (up to some order of ngram specified when the
        model is created.)
        """
        return self._ngrams

    @property
    def order(self) -> int:
        """
        Order of the highest order n-grams in the model.
        """
        return self._order

BEGIN_TOKEN = "<s>"
END_TOKEN = "</s>"

def _count(text: str, order: int) -> CountObject:
    """
    Return counts of all n-grams of order `order` and below.
    """
    counts: CountObject = [defaultdict(int) for _ in range(order)]
    assert not re.search(f"{re.escape(BEGIN_TOKEN)}|{re.escape(END_TOKEN)}", text), \
           f"Text cannot contain substrings '{BEGIN_TOKEN}'' or '{END_TOKEN}'."
    for sentence in sent_tokenize(text):
        words = [BEGIN_TOKEN, *word_tokenize(sentence), END_TOKEN]
        words_length = len(words)
        for i in range(words_length):
            for j in range(order):
                if i + j + 1 <= words_length:
                    counts[j][tuple(words[i:i+j+1])] += 1
    return counts

def _calculate_probabilities(counts: CountObject) -> NgramContainer:
    probabilities: NgramContainer = [defaultdict(float) for _ in range(len(counts))]
    unigrams = counts[0]
    total_unigrams = 0
    for number in unigrams.values():
        total_unigrams += number
    for i, ngram_count in enumerate(counts):
        for ngram in ngram_count:
            if i == 0:
                denominator = total_unigrams
            else:
                denominator = counts[i-1][ngram[:-1]]
            probabilities[i][ngram] = ngram_count[ngram] / denominator
    return probabilities
