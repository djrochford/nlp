"Ngram language model type and functions that operate on it."
module Ngram

import DataStructures.DefaultDict
import Languages.Language
import TextAnalysis.sentence_tokenize
import WordTokenizers.tokenize

export NgramModel

NgramContainer = Vector{Dict{Tuple{Vararg{String}}, Float64}}
CountContainer = Vector{Dict{Tuple{Vararg{String}}, Int}}

"""
    NgramModel(order::Int, corpus::String, language::Language)
    NgramModel(order::Int, corpus::Vector{Vector{String}})
Make an ngram-based language model, given the highest order of ngram and a training corpus.
The corpus can either be a pre-tokenised vector of sentences, each of which is a vector of
words, or it can be a single string. In the latter case, the NgramModel will tokenise the
string for you, but you have to specify the language of the string. You should do that using
an instance of the `Language` type, from the `Languages` package.
"""
struct NgramModel
    "The highest n of the ngrams in the model"
    order::Int
    """
    A vector of dicts with ngram keys, represented as tuples, and floats as values.
    The first dict has unigram keys, the second has bigram keys, and so on, up to `order`.
    The float values represent unconditional probabilities, in the case of unigrams, and
    conditional probabilities of the ngram, given it's prefix, in the case of higher-order
    ngrams.
    """
    ngrams::NgramContainer
    function NgramModel(order, ngrams)
        if maximum(map(length, keys(ngrams))) != order
            error("Ngrams have different order to `order` parameter.")
        else
            return new(order, ngrams)
        end
    end
end

function NgramModel(order::Int, ngram_count:: CountContainer)
    return NgramModel(order, calculate_probabilities(ngram_count))
end

function NgramModel(order::Int, corpus::String, language::Language)
    return NgramModel(order, ngram_count(order, corpus, language))
end

function calculate_probabilities(counts::CountContainer)::NgramContainer
    probabilities = [
        DefaultDict{Tuple{Vararg{String}}, Float64}(0.0) for _ = 1:length(counts)
    ]
    unigrams = counts[1]
    total_unigrams = 0
    for number in values(unigrams)
        total_unigrams += number
    end
    for (i, ngram_count) in enumerate(counts)
        for ngram in keys(ngram_count)
            if i == 1
                denominator = total_unigrams
            else
                denominator = counts[i - 1][reverse(Base.tail(reverse(ngram)))]
            end
            probabilities[i][ngram] = ngram_count[ngram] / denominator
        end
    end
    return probabilities
end

BEGIN_TOKEN = "<s>"
END_TOKEN = "</s>"

function ngram_count(order::Int, text::String, language::Language)::CountContainer
    counts = [DefaultDict{Tuple{Vararg{String}}, Int}(0) for _ = 1:order]
    for sentence in sentence_tokenize(language, text)
        words = [BEGIN_TOKEN, tokenize(sentence)..., END_TOKEN]
        words_length = length(words)
        for i = 1:words_length
            for j = 1:order
                if i + j - 1 <= words_length
                    counts[j][Tuple(words[i:i+j-1])] += 1
                end
            end
        end
    end
    return counts
end

end
