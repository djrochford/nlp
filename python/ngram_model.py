from nltk import sent_tokenize, word_tokenize
from collections import defaultdict, Counter
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Ngram_model:
  def __init__(self, training_text, highest_order):
    assert type(training_text) == str, "First parameter must be a string."
    assert type(highest_order) == int and highest_order > 0, "Second parameter must be an integer greater than 0."
    self.highest_order = highest_order
    self.counts_KN = self.make_KN_counts(training_text)
    self.discounts = self.make_discounts()
    self.backoffs = self.make_backoffs()
    self.model = []
    self.make_model()

  def calculate_count(self, text, n):
    sentences = sent_tokenize(text)
    count = defaultdict(int)
    for sentence in sentences:
      words = ['<s>', *word_tokenize(sentence), '</s>']
      for i in range(0, len(words)+1-n):
        ngram = tuple(words[i:i+n])
        count[ngram] += 1
    return count
  
  def make_KN_counts(self, text):
    counts = [self.calculate_count(text, self.highest_order)]
    for k in range(self.highest_order-1, 0, -1):
      k_counts = defaultdict(int)
      plus_counts = counts[-1]
      for gram in plus_counts:
        prefix = gram[:-1]
        k_counts[prefix] += 1
        if gram[-1] == '</s>':
          suffix = gram[1:]
          k_counts[suffix] += 1
      counts.append(k_counts)
    return counts

  def calculate_discount(self, k_num_with_counts, i, Y):
    if i == 0:
      return 0
    else: 
      if i > 3:
        i = 3
      return i - (i + 1)*Y*k_num_with_counts[i+1]/k_num_with_counts[i]

  def make_discounts(self):
    discounts = []
    for k_counts in self.counts_KN:
      k_num_with_counts = Counter(value for value in k_counts.values() if value <= 4)
      Y = k_num_with_counts[1]/(k_num_with_counts[1] + 2*k_num_with_counts[2])
      discounts.append({kgram: self.calculate_discount(k_num_with_counts, k_counts[kgram], Y) for kgram in k_counts})
    discounts.append({(): 0})
    return discounts

  def calculate_backoff(self, prefix):
    continuation_counts = self.counts_KN[self.highest_order - len(prefix) - 1]
    sum_counts = 0
    num_counts = 0
    for ngram, count in continuation_counts.items():
      if ngram[:-1] == prefix:
        sum_counts += count
        num_counts += 1
    discount = self.discounts[self.highest_order - len(prefix)][prefix]
    if discount == 0:
      return 0
    else:
      return (discount/sum_counts) * num_counts

  def make_backoffs(self):
    backoffs = []
    for kn_count in self.counts_KN[1:]:
      backoffs.append({ngram: self.calculate_backoff(ngram) for ngram in kn_count if ngram[-1] != '</s>'})
    backoffs.append({(): self.calculate_backoff(())})
    return backoffs

  def calculate_unadjusted_probability(self, word, prefix):
    if prefix == ():
      kn_count = self.counts_KN[-1][word]
      discount = self.discounts[-2][word]
    else:
      kn_count = self.counts_KN[self.highest_order - len(prefix)][prefix]
      discount = self.discounts[self.highest_order - len(prefix)][prefix]
    continuation_counts  = self.counts_KN[self.highest_order - len(prefix) - 1]
    sum_over_continuations = sum([count for ngram, count in continuation_counts.items() if ngram[:-1] == prefix])
    return max(kn_count - discount, 0) / sum_over_continuations

  def calculate_probability(self, ngram):
    prefix = ngram[:-1]
    word = ngram[-1]
    backoff = self.backoffs[self.highest_order - len(prefix) - 1][prefix]
    if prefix == ():
      interpolation = backoff * 1/len(self.counts_KN[-1])
    else:
      interpolation = backoff * self.model[-1][(*prefix[1:], word)]
    return self.calculate_unadjusted_probability((word,), prefix) + interpolation

  def make_model(self):
    for k in range(1, self.highest_order+1):
      kgram_probabilities = {}
      for ngram in self.counts_KN[self.highest_order - k]:
        print(ngram)
        probability = self.calculate_probability(ngram)
        kgram_probabilities[ngram] = probability
      self.model.append(kgram_probabilities)

  # def generate_sentence(self):



