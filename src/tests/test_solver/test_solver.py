import env

import unittest

from tests.testcase_based_on_data import TestCaseBasedOnData

from base.nonogram import Nonogram
from base.solution import Solution
from solver.solver import *
from solver.layout_index import LayoutIndex

class TestSolver(TestCaseBasedOnData):
    def test_solve_and_compare(self):
        test_data = self.getSolutionData()
        mySolver = Solver()

        for layout, solution in test_data:
            s0 = Solution.load_from_file(solution)
            print s0

            n0 = Nonogram.load_from_file(layout)
            s1 = mySolver.solve(n0)
            print s1

            self.assertEqual(s0, s1)

class TestSolveMethod(TestCaseBasedOnData):
    #
    # find nearest pos
    #
    def test_find_nearest_pos_1(self):
        # index, layout, line
        li1 = LayoutIndex(3, 991)
        r = SolveMethod.find_nearest_pos(li1, [-1, -1, 1, 1, 1, -1])
        self.assertEqual(r, 2)

    def test_find_nearest_pos_2(self):
        # index, layout, line
        li1 = LayoutIndex(3, 991)
        r = SolveMethod.find_nearest_pos(li1, [-1, -1, -1, 1, 1, -1])
        self.assertEqual(r, 2)

    def test_find_nearest_pos_3(self):
        # index, layout, line
        li1 = LayoutIndex(2, 991)
        self.assertRaises(IndexOutOfRange, SolveMethod.find_nearest_pos, li1, [-1, -1, 1, 1, 1, -1])

    def test_find_nearest_pos_4(self):
        # index, layout, line
        li1 = LayoutIndex(3, 991)
        r = SolveMethod.find_nearest_pos(li1, [-1, -1, -1, 1, 1, 1])
        self.assertEqual(r, 3)


    #
    # fill line
    #
    def test_fill_when_input_line_is_empty(self):
        li1 = LayoutIndex(1, 991)
        li2 = LayoutIndex(2, 992)
        r = SolveMethod.fill_line([li1, li2], [-1, -1, -1, -1, -1, -1], 1)

        self.assertEqual(r, [li1, (li1, li2), li2, li2, (li2, None), (li2, None)])

    def test_fill_when_layout_need_more_than_nessasary(self):
        li1 = LayoutIndex(2, 991)
        li2 = LayoutIndex(3, 992)

        self.assertRaises(LineOutOfRange, SolveMethod.fill_line, [li1, li2], [-1, -1, -1, -1, -1], 1)

    def test_fill_full_line_1(self):
        li1 = LayoutIndex(2, 991)
        li2 = LayoutIndex(1, 992)
        r = SolveMethod.fill_line([li1, li2], [-1, -1, -1, -1], 1)

        self.assertEqual(r, [li1, li1, (li1, li2), li2])

    def test_fill_full_line_2(self):
        li1 = LayoutIndex(2, 991)
        r = SolveMethod.fill_line([li1], [-1, -1, 0, -1], 1)

        self.assertEqual(r, [li1, li1, (li1, None), (li1, None)])

    def test_fill_full_line_3(self):
        li1 = LayoutIndex(2, 991)
        r = SolveMethod.fill_line([li1], [-1, 0, -1, -1], 1)

        self.assertEqual(r, [(li1, None), (li1, None), li1, li1])

    def test_fill_full_line_4(self):
        r = SolveMethod.fill_line([], [-1, -1, -1, -1], 1)
        self.assertEqual(r, [(None, None)]*4)

    def test_fill_full_line_5(self):
        li1 = LayoutIndex(2, 991)
        r = SolveMethod.fill_line([li1], [-1, -1, 1, -1], 1)

        self.assertEqual(r, [(li1, None), li1, li1, (li1, None)])

    def test_fill_full_line_6(self):
        li1 = LayoutIndex(3, 991)
        r = SolveMethod.fill_line([li1], [-1, 1, 1, 1], 1)

        self.assertEqual(r, [(li1, None), li1, li1, li1])

    #
    # find intersection
    #
    def test_find_intersection_x5_l3(self):
        li1 = LayoutIndex(3, 991)
        r = SolveMethod.find_intersection([li1], [-1, -1, -1, -1, -1], 1)

        self.assertEqual(r, [None, None, 1, None, None])

    def test_find_intersection_x4_l2(self):
        li1 = LayoutIndex(2, 991)
        r = SolveMethod.find_intersection([li1], [-1, -1, -1, -1], 1)

        self.assertEqual(r, [None, None, None, None])

    def test_find_intersection_x4_l2(self):
        li1 = LayoutIndex(2, 991)
        r = SolveMethod.find_intersection([li1], [-1, -1, 0, -1], 1)

        self.assertEqual(r, [1, 1, 0, 0])

    def test_find_intersection_x4_l2a1(self):
        li1 = LayoutIndex(2, 991)
        li2 = LayoutIndex(1, 992)
        r = SolveMethod.find_intersection([li1, li2], [-1, -1, -1, -1], 1)

        self.assertEqual(r, [1, 1, 0, 1])

if __name__ == '__main__':
    unittest.main()