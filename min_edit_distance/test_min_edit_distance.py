"""
Tests for functions in min_edit_distance.py
"""
from typing import List, Tuple
from unittest import TestCase

import numpy as np  # type: ignore

from min_edit_distance import AlignmentColumn, DistanceCell, Edit, align_to_string, extract_traces, trace_to_alignment


def list_to_distance_matrix(
        matrix: List[List[Tuple[int, List[Tuple[int, int]]]]]
) -> np.array:
    """
    Convenience method for making inputs of the type expected by
    `test_extract_traces`.
    """
    return np.array([
        [DistanceCell(distance=cell[0], previous=cell[1]) for cell in row]
        for row in matrix
    ])


class TestExtracttTraces(TestCase):
    def test_null_case(self):
        null_case = list_to_distance_matrix([[(0, [])]])
        self.assertEqual(extract_traces(null_case), [[]])

    def test_single_insertion(self):
        single_insertion = list_to_distance_matrix([[(0, []), (1, [(0, 0)])]])
        self.assertEqual(extract_traces(single_insertion), [[(0, 1)]])

    def test_single_deletion(self):
        single_deletion = list_to_distance_matrix([[(0, [])],
                                                   [(1, [(0, 0)])]])
        self.assertEqual(extract_traces(single_deletion), [[(1, 0)]])

    def test_two_by_two(self):
        two_by_two = list_to_distance_matrix([[(0, []), (1, [(0, 0)])],
                                              [(1, [(0, 0)]), (2, [(0, 1), (1, 0)])]])
        traces = extract_traces(two_by_two)
        self.assertEqual(len(traces), 2)
        self.assertIn([(0, 1), (1, 1)], traces)
        self.assertIn([(1, 0), (1, 1)], traces)

    def test_up_and_left(self):
        up_and_left = list_to_distance_matrix([[(0, []), (1, [(0, 0)]), (2, [(1, 0)])],
                                               [(1, [(0, 0)]), (2, [(1, 0), (0, 1)]), (3, [(2, 0), (1, 1)])],
                                               [(2, [(1, 0)]), (3, [(1, 1), (2, 0)]), (4, [(1, 2), (2, 1)])]])
        traces = extract_traces(up_and_left)
        self.assertEqual(len(traces), 6)

class TestTraceToAligment(TestCase):
    def test_null_case(self):
        self.assertEqual(trace_to_alignment([], source="", target=""), [])

    def test_single_insertion(self):
        self.assertEqual(
            trace_to_alignment([(0, 1)], source="", target="I"),
            [AlignmentColumn(source_char=None, target_char="I", edit=Edit.INSERTION)]
        )

    def test_single_deletion(self):
        self.assertEqual(
            trace_to_alignment([(1, 0)], source="I", target=""),
            [AlignmentColumn(source_char="I", target_char=None, edit=Edit.DELETION)]
        )

    def test_single_substitution(self):
        self.assertEqual(
            trace_to_alignment([(1, 1)], source="I", target="U"),
            [AlignmentColumn(source_char="I", target_char = "U", edit=Edit.SUBSTITUTION)]
        )

    def test_intention_execution(self):
        trace = [(1, 0), (2, 1), (3, 2), (4, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]
        alignment = trace_to_alignment(trace, source="intention", target="execution")
        expected_source_chars = ["i", "n", "t", "e", None, "n", "t", "i", "o", "n"]
        expected_target_chars = [None, "e", "x", "e", "c", "u", "t", "i", "o", "n"]
        expected_edits = [Edit.DELETION, Edit.SUBSTITUTION, Edit.SUBSTITUTION, None, Edit.INSERTION, Edit.SUBSTITUTION, None, None, None, None]
        for i, column in enumerate(alignment):
            self.assertEqual(column.source_char, expected_source_chars[i])
            self.assertEqual(column.target_char, expected_target_chars[i])
            self.assertEqual(column.edit, expected_edits[i])

class TestAlignToString(TestCase):
    def test_null_case(self):
        self.assertEqual(align_to_string([]), "\n\n")

    def test_single_insertion(self):
        self.assertEqual(align_to_string([AlignmentColumn(source_char=None, target_char="E", edit=Edit.INSERTION)]), "*\nE\ni")

    def test_single_deletion(self):
        self.assertEqual(align_to_string([AlignmentColumn(source_char="I", target_char=None, edit=Edit.DELETION)]), "I\n*\nd")

    def test_single_substitution(self):
        self.assertEqual(align_to_string([AlignmentColumn(source_char="I", target_char="E", edit=Edit.SUBSTITUTION)]), "I\nE\ns")

    def test_intention_execution(self):
        trace = [(1, 0), (2, 1), (3, 2), (4, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]
        alignment = trace_to_alignment(trace, source="INTENTION", target="EXECUTION")
        self.assertEqual(align_to_string(alignment), "INTE*NTION\n*EXECUTION\ndss is    ")
