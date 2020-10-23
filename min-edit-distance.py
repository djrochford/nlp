"""
Implementation of minimum edit distance algorithm, following Jurafsy & Martin,
Chapter 2
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional, Set, Tuple

import numpy as np


def one(_char: str) -> int:
    """
    Constant function, used as default deletion and insertion cost function.
    """
    return 1


def zero_or_two(char_src: str, char_tar: str) -> int:
    """
    Used as default substituion cost function.
    """
    if char_src == char_tar:
        return 0
    return 2


class Edit(Enum):
    DELETION = "d"
    INSERTION = "i"
    SUBSTITUTION = "s"


@dataclass
class AlignmentColumn:
    source_char: Optional[str]
    target_char: Optional[str]
    edit: Optional[Edit]


Alignment = List[AlignmentColumn]


def min_edit_distance(
        source: str,
        target: str,
        *,
        del_cost: Callable[[str], int] = one,
        ins_cost: Callable[[str], int] = one,
        sub_cost: Callable[[str, str], int] = zero_or_two
) -> Tuple[int, Set[Alignment]]:

    n = len(source)
    m = len(target)
    distance = np.zeros((n+1, m+1), dtype=DistanceCell)

    distance[0, 0] = DistanceCell(0, None)
    for i in range(1, n+1):
        distance[i, 0] = DistanceCell(
            distance[i-1, 0].distance + del_cost(source[i-1]), [(i-1, 0)]
        )
    for j in range(1, m+1):
        distance[0, j] = DistanceCell(
            distance[0, j-1].distance + ins_cost(target[j-1]), [(0, j-1)]
        )

    for i in range(1, n+1):
        for j in range(1, m+1):
            via_deletion = distance[i-1, j].distance + del_cost(source[i-1])
            via_insertion = distance[i, j-1].distance + ins_cost(target[j-1])
            via_substitution = (
                distance[i-1, j-1].distance
                + sub_cost(source[i-1], target[j-1])
            )
            minimum = min(via_deletion, via_insertion, via_substitution)
            distance[i, j] = DistanceCell(distance=minimum)
            if minimum == via_deletion:
                distance[i, j].previous.append((i-1, j))
            if minimum == via_insertion:
                distance[i, j].previous.append((i, j-1))
            if minimum == via_substitution:
                distance[i, j].previous.append((i-1, j-1))

    alignments = [
        trace_to_alignment(trace, source, target)
        for trace in extract_traces(distance)
    ]
    return distance[n, m].distance, alignments


Address = Tuple[int, int]

Trace = List[Address]


def extract_traces(matrix: np.array) -> List[Trace]:
    traces = []

    def traverse_tree(current_trace: Trace, current_address: Address):
        i, j = current_address
        previous_addresses = matrix[i, j].previous
        if previous_addresses:
            current_trace.append(current_address)
            for address in previous_addresses:
                traverse_tree(list(current_trace), address)
        else:
            current_trace.reverse()
            traces.append(current_trace)
    n_plus, m_plus = matrix.shape
    traverse_tree([], (n_plus - 1, m_plus - 1))
    return traces


def trace_to_alignment(trace: Trace, source: str, target: str) -> Alignment:
    alignment = []
    previous = (0, 0)
    for address in trace:
        i_prev, j_prev = previous
        i, j = address
        source_char = source[i-1]
        target_char = target[j-1]
        if i_prev == i:
            align = AlignmentColumn(
                source_char=None, target_char=target_char, edit=Edit.INSERTION
            )
        elif j_prev == j:
            align = AlignmentColumn(
                source_char=source_char, target_char=None, edit=Edit.DELETION
            )
        else:
            if source_char == target_char:
                align = AlignmentColumn(
                    source_char=source_char, target_char=target_char, edit=None
                )
            else:
                align = AlignmentColumn(
                    source_char=source_char,
                    target_char=target_char,
                    edit=Edit.SUBSTITUTION
                )
        previous = address
        alignment.append(align)
    print(trace)
    print(align_to_string(alignment))
    return alignment


@dataclass
class DistanceCell:
    distance: int
    previous: List[Tuple[int, int]] = field(default_factory=list)


def align_to_string(alignment: Alignment) -> str:
    source = ""
    target = ""
    edits = ""
    for align in alignment:
        source += align.source_char or "*"
        target += align.target_char or "*"
        edits += (align.edit and align.edit.value) or " "
    return f"{source}\n{target}\n{edits}"
