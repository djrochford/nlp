module TestNgram

using Test
import Languages.English

include("ngram.jl")
import .Ngram: BEGIN_TOKEN, END_TOKEN, CountContainer, ngram_count

SIMPLE_CORPUS = "I am Sam. Sam I am. I do not like green eggs and ham."

function run_unigram_test(count_vec::CountContainer)::Nothing
    @testset "ngram_count -- unigram" begin
        unigrams = count_vec[1]
        @test length(unigrams) == 13

        expected_grams = Set([
            (BEGIN_TOKEN,),
            ("I",),
            ("am",),
            ("Sam",),
            (".",),
            (END_TOKEN,),
            ("do",),
            ("not",),
            ("like",),
            ("green",),
            ("eggs",),
            ("and",),
            ("ham",),
        ])
        @test keys(unigrams) == expected_grams

        for gram in expected_grams
            count = unigrams[gram]
            if gram in [(BEGIN_TOKEN,), ("I",), (".",), (END_TOKEN,)]
                @test count == 3
            elseif gram in [("am",), ("Sam",)]
                @test count == 2
            else
                @test count == 1
            end
        end
    end
    return nothing
end

function run_bigram_test(count_vec::CountContainer)::Nothing
    @testset "ngram_count -- bigram" begin
        bigrams = count_vec[2]
        @test length(bigrams) == 16
        expected_grams = Set([
            (BEGIN_TOKEN, "I"),
            ("I", "am"),
            ("am", "Sam"),
            ("Sam", "."),
            (".", END_TOKEN),
            (BEGIN_TOKEN, "Sam"),
            ("Sam", "I"),
            ("am", "."),
            ("I", "do"),
            ("do", "not"),
            ("not", "like"),
            ("like", "green"),
            ("green", "eggs"),
            ("eggs", "and"),
            ("and", "ham"),
            ("ham", "."),
        ])
        @test keys(bigrams) == expected_grams
        for gram in expected_grams
            count = bigrams[gram]
            if gram == (".", END_TOKEN)
                @test count == 3
            elseif gram in [(BEGIN_TOKEN, "I"), ("I", "am")]
                @test count == 2
            else
                @test count == 1
            end
        end
        run_unigram_test(count_vec)
    end
    return nothing
end

function run_trigram_test(count_vec::CountContainer)::Nothing
    @testset "ngram_count -- trigram" begin
        trigrams = count_vec[3]
        @test length(trigrams) == 17
        expected_grams = Set([
            (BEGIN_TOKEN, "I", "am"),
            ("I", "am", "Sam"),
            ("am", "Sam", "."),
            ("Sam", ".", END_TOKEN),
            (BEGIN_TOKEN, "Sam", "I"),
            ("Sam", "I", "am"),
            ("I", "am", "."),
            ("am", ".", END_TOKEN),
            (BEGIN_TOKEN, "I", "do"),
            ("I", "do", "not"),
            ("do", "not", "like"),
            ("not", "like", "green"),
            ("like", "green", "eggs"),
            ("green", "eggs", "and"),
            ("eggs", "and", "ham"),
            ("and", "ham", "."),
            ("ham", ".", END_TOKEN),
        ])
        @test keys(trigrams) == expected_grams
        for gram in expected_grams
            @test trigrams[gram] == 1
        end
        run_bigram_test(count_vec)
    end
    return nothing
end


ORDER_TO_FUNCTION =
    Dict{Int,Function}(1 => run_unigram_test, 2 => run_bigram_test, 3 => run_trigram_test)

function run_gram_test(order::Int)::Nothing
    count_vec = ngram_count(order, SIMPLE_CORPUS, English())
    ORDER_TO_FUNCTION[order](count_vec)
    return nothing
end

run_gram_test(1)
run_gram_test(2)
run_gram_test(3)

end
