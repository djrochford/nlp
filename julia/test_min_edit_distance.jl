module TestMinEditDistance

using Test
include("min_edit_distance.jl")
import .MinEditDistance:
    Alignment,
    AlignmentColumn,
    DistanceTable,
    DistanceCell,
    Trace,
    deletion,
    extract_traces,
    insertion,
    min_edit_distance,
    no_edit,
    substitution,
    trace_to_alignment

@testset "extract_traces" begin
    null_cell = DistanceCell(0, Set())
    one_step_cell = DistanceCell(1, Set([(1, 1)]))

    null_table = DistanceTable(undef, 1, 1)
    null_table[1, 1] = null_cell
    @test extract_traces(null_table) == Set()

    single_insertion_table = DistanceTable(undef, 1, 2)
    single_insertion_table[1, 1] = null_cell
    single_insertion_table[1, 2] = one_step_cell
    @test extract_traces(single_insertion_table) == Set([[(1, 2)]])

    single_deletion_table = DistanceTable(undef, 2, 1)
    single_deletion_table[1, 1] = null_cell
    single_deletion_table[2, 1] = one_step_cell
    @test extract_traces(single_deletion_table) == Set([[(2, 1)]])

    two_by_two_cell = DistanceCell(2, Set([(1, 2), (2, 1)]))
    two_by_two = [
        null_cell one_step_cell
        one_step_cell two_by_two_cell
    ]
    @test extract_traces(two_by_two) == Set([[(1, 2), (2, 2)], [(2, 1), (2, 2)]])

    up_and_left = [
        null_cell one_step_cell DistanceCell(2, Set([(1, 2)]))
        one_step_cell two_by_two_cell DistanceCell(3, Set([(1, 3), (2, 2)]))
        DistanceCell(2, Set([(2, 1)])) DistanceCell(3, Set([(3, 1), (2, 2)])) DistanceCell(4, Set([(3, 2), (2, 3)]))
    ]
    @test length(extract_traces(up_and_left)) == 6
end

@testset "trace_to_alignment" begin
    @test trace_to_alignment(Trace(), "", "") == Alignment()
    @test trace_to_alignment([(1, 2)], "", "E") ==
          [AlignmentColumn(; source_char=nothing, target_char='E', edit=insertion)]
    @test trace_to_alignment([(2, 1)], "I", "") ==
          [AlignmentColumn(; source_char='I', target_char=nothing, edit=deletion)]
    @test trace_to_alignment([(2, 2)], "I", "E") ==
          [AlignmentColumn(; source_char='I', target_char='E', edit=substitution)]
    @test trace_to_alignment([(2, 2)], "I", "I") ==
          [AlignmentColumn(; source_char='I', target_char='I', edit=no_edit)]

    trace =
        trace = [
            (2, 1), (3, 2), (4, 3), (5, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
        ]
    alignment = trace_to_alignment(trace, "intention", "execution")
    expected_source_chars = ['i', 'n', 't', 'e', nothing, 'n', 't', 'i', 'o', 'n']
    expected_target_chars = [nothing, 'e', 'x', 'e', 'c', 'u', 't', 'i', 'o', 'n']
    expected_edits = [
        deletion,
        substitution,
        substitution,
        no_edit,
        insertion,
        substitution,
        no_edit,
        no_edit,
        no_edit,
        no_edit,
    ]
    for (i, column) in enumerate(alignment)
        @test column.source_char == expected_source_chars[i]
        @test column.target_char == expected_target_chars[i]
        @test column.edit == expected_edits[i]
    end
end

@testset "show's Alignment method" begin
    @test show(Alignment()) == "\n\n"
    @test show([AlignmentColumn(; source_char=nothing, target_char='E', edit=insertion)]) ==
          "*\nE\ni"
    @test show([AlignmentColumn(; source_char='I', target_char=nothing, edit=deletion)]) ==
          "I\n*\nd"
    @test show([AlignmentColumn(; source_char='I', target_char='E', edit=substitution)]) ==
          "I\nE\ns"

    trace = [
        (2, 1), (3, 2), (4, 3), (5, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
    ]
    alignment = trace_to_alignment(trace, "INTENTION", "EXECUTION")
    @test show(alignment) == "INTE*NTION\n*EXECUTION\ndss is    "
end

@testset "min_edit_distance" begin
    @test min_edit_distance(; source="", target="") == (0, Set{Alignment}())

    single_insert_dis, single_insert_alignment = min_edit_distance(; source="", target="E")
    @test single_insert_dis == 1
    @test length(single_insert_alignment) == 1
    @test show(first(single_insert_alignment)) == "*\nE\ni"

    single_delete_dis, single_delete_alignment = min_edit_distance(; source="I", target="")
    @test single_delete_dis == 1
    @test length(single_delete_alignment) == 1
    @test show(first(single_delete_alignment)) == "I\n*\nd"

    single_sub_dis, single_sub_alignment = min_edit_distance(; source="I", target="E")
    @test single_sub_dis == 2
    @test length(single_sub_alignment) == 3
    @test Set(["*I\nE*\nid", "I*\n*E\ndi", "I\nE\ns"]) ==
          Set([show(align) for align in single_sub_alignment])

    int_ext_distance, int_ext_alignments = min_edit_distance(;
        source="INTENTION", target="EXECUTION"
    )
    @test int_ext_distance == 8
    @test "INTE*NTION\n*EXECUTION\ndss is    " in
          Set([show(align) for align in int_ext_alignments])
end

end
