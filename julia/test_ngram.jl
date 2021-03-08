module TestNgram

using Test
import DataStructures.DefaultDict
import Languages.English

include("ngram.jl")
import .Ngram: BEGIN_TOKEN, END_TOKEN, CountContainer, ngram_count

SIMPLE_CORPUS = "I am Sam. Sam I am. I do not like green eggs and ham."

EXPECTED_GRAMS = [
    Set([
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
    ]),
    Set([
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
    ]),
    Set([
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
    ]),
]

EXPECTED_COUNTS = [
    Dict(
        (BEGIN_TOKEN,) => 3,
        ("I",) => 3,
        (".",) => 3,
        (END_TOKEN,) => 3,
        ("am",) => 2,
        ("Sam",) => 2,
    ),
    Dict((".", END_TOKEN) => 3, (BEGIN_TOKEN, "I") => 2, ("I", "am") => 2),
    Dict(),
]

function run_ngram_count_test(order::Int, count_vec::CountContainer)::Nothing
    if order == 0
        return nothing
    end
    @testset "ngram_count -- order $order" begin
        grams = count_vec[order]
        expected_grams = EXPECTED_GRAMS[order]
        @test length(grams) == length(expected_grams)
        @test keys(grams) == expected_grams
        expected_counts = EXPECTED_COUNTS[order]
        for gram in expected_grams
            @test grams[gram] == get(expected_counts, gram, 1)
        end
    end
    run_ngram_count_test(order - 1, count_vec)
end

function run_ngram_count_test(order::Int)::Nothing
    count_vec = ngram_count(order, SIMPLE_CORPUS, English())
    run_ngram_count_test(order, count_vec)
    return nothing
end

run_ngram_count_test(1)
run_ngram_count_test(2)
run_ngram_count_test(3)

end
