module TestMinEditDistance

using Test
include("min_edit_distance.jl")
using .MinEditDistance
import .MinEditDistance: Alignment, AlignmentColumn, deletion

@test min_edit_distance(source="", target="") == (0, Set{Alignment}())
@test min_edit_distance(source="I", target="") == (
    1,
    Set([[AlignmentColumn(source_char='I', target_char=nothing, edit=deletion)]])
)

end
