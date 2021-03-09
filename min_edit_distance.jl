"""
Implementation of minimum edit distance algorithm, following Jurafsy & Martin, Chapter 2
"""
module MinEditDistance
import Base.@kwdef
export min_edit_distance

char_to_one(c::Char) = 1
zero_or_two(c1::Char, c2::Char) = c1 == c2 ? 0 : 2

@enum Edit deletion insertion substitution no_edit

@kwdef struct AlignmentColumn
    source_char::Union{Char,Nothing}
    target_char::Union{Char,Nothing}
    edit::Edit
end

Alignment = Vector{AlignmentColumn}

Address = Tuple{Int,Int}
Trace = Vector{Address}

struct DistanceCell
    distance::Int
    previous::Set{Address}
end

DistanceTable = Array{DistanceCell,2}

"""
    min_edit_distance(source, target, del_cost, ins_cost, sub_cost)

Compute the minimum edit distance between `source` and `target` strings, using
`del_cost`, `ins_cost` and `sub_cost` Functions to calculate the cost of deletions,
insertions and substitutions, respectively.

`del_cost` and `ins_cost` must take a Char and return an Integer; by default they are
the function that returns 1 for every Char. `sub_cost` takes two Char arguments and
return an Integer; by default, it's the Function that returns 0 when it's arguments are
equal, and 2 otherwise.
"""
function min_edit_distance(;
    source::AbstractString,
    target::AbstractString,
    del_cost::Function=char_to_one,
    ins_cost::Function=char_to_one,
    sub_cost::Function=zero_or_two,
)::Tuple{Int,Set{Alignment}}
    n = length(source)
    m = length(target)
    distance_table = DistanceTable(undef, n + 1, m + 1)
    distance_table[1, 1] = DistanceCell(0, Set{Address}())
    for i in 2:(n + 1)
        distance_table[i, 1] = DistanceCell(
            distance_table[i - 1, 1].distance + del_cost(source[i - 1]), Set([(i - 1, 1)])
        )
    end
    for j in 2:(m + 1)
        distance_table[1, j] = DistanceCell(
            distance_table[1, j - 1].distance + ins_cost(target[j - 1]), Set([(1, j - 1)])
        )
    end
    for i in 2:(n + 1)
        for j in 2:(m + 1)
            via_deletion = distance_table[i - 1, j].distance + del_cost(source[i - 1])
            via_insertion = distance_table[i, j - 1].distance + ins_cost(target[j - 1])
            via_substitution =
                distance_table[i - 1, j - 1].distance +
                sub_cost(source[i - 1], target[j - 1])
            min = minimum([via_deletion, via_insertion, via_substitution])
            distance_table[i, j] = DistanceCell(min, Set{Address}())
            if min == via_deletion
                push!(distance_table[i, j].previous, (i - 1, j))
            end
            if min == via_insertion
                push!(distance_table[i, j].previous, (i, j - 1))
            end
            if min == via_substitution
                push!(distance_table[i, j].previous, (i - 1, j - 1))
            end
        end
    end
    alignments = Set([
        trace_to_alignment(trace, source, target)
        for trace in extract_traces(distance_table)
    ])
    return (distance_table[n + 1, m + 1].distance, alignments)
end

function extract_traces(table::DistanceTable)::Set{Trace}
    traces = Set{Trace}()
    function traverse_table(current_trace::Trace, current_address::Address)
        i, j = current_address
        previous_addresses = table[i, j].previous
        if isempty(previous_addresses)
            if !isempty(current_trace)
                push!(traces, reverse(current_trace))
            end
        else
            push!(current_trace, current_address)
            for address in previous_addresses
                traverse_table(Trace(current_trace), address)
            end
        end
    end
    traverse_table(Trace(), size(table))
    return traces
end

function trace_to_alignment(
    trace::Trace, source::AbstractString, target::AbstractString
)::Alignment
    alignment = Alignment()
    previous = (1, 1)
    for address in trace
        i_prev, j_prev = previous
        i, j = address
        if i_prev == i
            align = AlignmentColumn(;
                source_char=nothing, target_char=target[j - 1], edit=insertion
            )
        elseif j_prev == j
            align = AlignmentColumn(;
                source_char=source[i - 1], target_char=nothing, edit=deletion
            )
        else
            source_char = source[i - 1]
            target_char = target[j - 1]
            if source_char == target_char
                align = AlignmentColumn(;
                    source_char=source_char, target_char=target_char, edit=no_edit
                )
            else
                align = AlignmentColumn(;
                    source_char=source_char, target_char=target_char, edit=substitution
                )
            end
        end
        previous = address
        push!(alignment, align)
    end
    return alignment
end

function Base.show(io::IO, alignment::Alignment)
    source = ""
    target = ""
    edits = ""
    edit_to_char = Dict(
        insertion => 'i', deletion => 'd', substitution => 's', no_edit => ' '
    )
    for align in alignment
        source *= isnothing(align.source_char) ? "*" : align.source_char
        target *= isnothing(align.target_char) ? "*" : align.target_char
        edits *= edit_to_char[align.edit]
    end
    return "$source\n$target\n$edits"
end

end
