"""
Tests for functions in min_edit_distance.py
"""
from typing import List, Tuple
from unittest import TestCase

import numpy as np  # type: ignore

from min_edit_distance import DistanceCell, extract_traces


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

    def test_up_and_right(self):
        up_and_right = list_to_distance_matrix([[(0, []), (1, [(0, 0)]), (2, [(1, 0)])],
                                                [(1, [(0, 0)]), (2, [(1, 0), (0, 1)]), (3, [(2, 0), (1, 1)])],
                                                [(2, [(1, 0)]), (3, [(1, 1), (2, 0)]), (4, [(1, 2), (2, 1)])]])
        traces = extract_traces(up_and_right)
        self.assertEqual(len(traces), 6)