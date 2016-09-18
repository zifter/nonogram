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

            self.assertEqual(s0, s1, "Solution failed: %s" % solution)

class TestSolveMethod(TestCaseBasedOnData):
    def test_cells_amount_1(self):
        li1 = LayoutIndex(3)
        r = SolveMethod.cells_amount([li1], 1)
        self.assertEqual(r, 3)

    def test_cells_amount_2(self):
        li1 = LayoutIndex(3)
        li2 = LayoutIndex(6)
        r = SolveMethod.cells_amount([li1, li2], 1)
        self.assertEqual(r, 10)

    def test_cells_amount_3(self):
        li1 = LayoutIndex(3)
        li2 = LayoutIndex(6)
        r = SolveMethod.cells_amount([li1, li2], 0)
        self.assertEqual(r, 9)

    def test_cells_amount_4(self):
        li1 = LayoutIndex(3)
        li2 = LayoutIndex(6)
        li3 = LayoutIndex(13)
        r = SolveMethod.cells_amount([li1, li2, li3], 1)
        self.assertEqual(r, 24)
    #
    # check line
    #
    def test_get_suitable_line_up_1(self):
        li1 = LayoutIndex(2)
        r = SolveMethod.get_suitable_line_up(li1, [-1, -1, -1], 1)

        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], [li1, li1, -1])
        self.assertEqual(r[1], [-1, li1, li1])

    def test_get_suitable_line_up_2(self):
        li1 = LayoutIndex(2)
        r = SolveMethod.get_suitable_line_up(li1, [-1, -1, 0, -1], 1)

        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], [li1, li1, 0, -1])

    def test_get_suitable_line_up_3(self):
        li1 = LayoutIndex(4)
        r = SolveMethod.get_suitable_line_up(li1, [-1, -1, 0, -1], 1)

        self.assertEqual(r, [])

    def test_get_suitable_line_up_4(self):
        li1 = LayoutIndex(2)
        r = SolveMethod.get_suitable_line_up(li1, [-1, -1], 1)

        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], [li1, li1])

    def test_get_suitable_line_up_5(self):
        li1 = LayoutIndex(3)
        self.assertRaises(LineOutOfRange, SolveMethod.get_suitable_line_up, li1, [-1, -1], 1)

    def test_get_suitable_line_up_6(self):
        li1 = LayoutIndex(2)
        r = SolveMethod.get_suitable_line_up(li1, [1, -1, -1, -1, -1], 1)

        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], [li1, li1, -1, -1, -1])

    def test_get_suitable_line_up_7(self):
        li1 = LayoutIndex(2)
        r = SolveMethod.get_suitable_line_up(li1, [-1, 1, -1, -1, -1, -1], 1)

        self.assertEqual(len(r), 2)
        self.assertEqual(r[0], [li1, li1, -1, -1, -1, -1])
        self.assertEqual(r[1], [-1, li1, li1, -1, -1, -1])

    def test_get_suitable_line_up_8(self):
        li1 = LayoutIndex(1)
        r = SolveMethod.get_suitable_line_up(li1, [-1, 1], 1)

        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], [-1, li1])

    #
    # merge line ups
    #
    def test_merge_lineups_1(self):
        r = SolveMethod.merge_lineups(
            [[1, 1, -1, -1, -1],
            [-1, 1, 1, -1, -1]]
        )
        self.assertEqual(r, [None, 1, None, -1, -1])

    #
    # find offset from end
    #
    def test_get_minimum_offset_1(self):
        li1 = LayoutIndex(1)
        offset = SolveMethod.get_minimum_offset(li1, [0, 0, -1, -1, -1], 1)
        self.assertEqual(offset, 4)

    def test_get_minimum_offset_2(self):
        li1 = LayoutIndex(1)
        offset = SolveMethod.get_minimum_offset(li1, [-1, -1, -1, -1, -1], 1)
        self.assertEqual(offset, 2)

    def test_get_minimum_offset_3(self):
        li1 = LayoutIndex(1)
        offset = SolveMethod.get_minimum_offset(li1, [-1, 1, -1, -1, -1], 1)
        self.assertEqual(offset, 3)

    #
    # find offset from end
    #
    def test_get_offset_from_end_1(self):
        li1 = LayoutIndex(1)
        (offset, layout) = SolveMethod.get_offset_from_end([li1], [-1, -1, -1, 1], 1)
        self.assertEqual(offset, 2)
        self.assertEqual(layout, [])

    def test_get_offset_from_end_2(self):
        li1 = LayoutIndex(1)
        (offset, layout) = SolveMethod.get_offset_from_end([li1], [-1, -1, 1, -1], 1)
        self.assertEqual(offset, 3)
        self.assertEqual(layout, [])

    def test_get_offset_from_end_3(self):
        li1 = LayoutIndex(1)
        (offset, layout) = SolveMethod.get_offset_from_end([li1], [-1, -1, -1, -1], 1)
        self.assertEqual(offset, 2)
        #self.assertEqual(layout, [li1])

    def test_get_offset_from_end_4(self):
        li1 = LayoutIndex(3)
        (offset, layout) = SolveMethod.get_offset_from_end([li1], [-1, -1, 1, -1, -1, -1], 1)
        self.assertEqual(offset, 5)
        #self.assertEqual(layout, [li1])

    def test_get_offset_from_end_5(self):
        li1 = LayoutIndex(2)
        (offset, layout) = SolveMethod.get_offset_from_end([li1], [-1, -1, 1, -1, 0, -1], 1)
        self.assertEqual(offset, 5)
        #self.assertEqual(layout, [li1])

    def test_get_offset_from_end_6(self):
        li1 = LayoutIndex(2)
        li2 = LayoutIndex(1)
        (offset, layout) = SolveMethod.get_offset_from_end([li1, li2], [-1, -1, -1, 1, 1, -1, 1, -1], 1)
        self.assertEqual(offset, 6)
        #self.assertEqual(layout, [])

    #
    # find nearest pos
    #
    def test_get_offset_from_start_1(self):
        # index, layout, line
        li1 = LayoutIndex(3)
        r = SolveMethod.get_offset_from_start(li1, [-1, -1, 1, 1, 1, -1], False)
        self.assertEqual(r, 2)

    def test_get_offset_from_start_2(self):
        # index, layout, line
        li1 = LayoutIndex(3)
        r = SolveMethod.get_offset_from_start(li1, [-1, -1, -1, 1, 1, -1], False)
        self.assertEqual(r, 2)

    def test_get_offset_from_start_3(self):
        # index, layout, line
        li1 = LayoutIndex(3)
        r = SolveMethod.get_offset_from_start(li1, [-1, -1, -1, 1, 1, 1], False)
        self.assertEqual(r, 3)

    def test_get_offset_from_start_4(self):
        li1 = LayoutIndex(2)
        self.assertRaises(IndexOutOfRange, SolveMethod.get_offset_from_start, li1, [-1, 1, 1, 1, 1, -1], False)

    def test_get_offset_from_start_5(self):
        # index, layout, line
        li1 = LayoutIndex(3)
        r = SolveMethod.get_offset_from_start(li1, [-1, -1, -1, -1, 1, 1], True)
        self.assertEqual(r, 0)

    def test_get_offset_from_start_6(self):
        # index, layout, line
        li1 = LayoutIndex(3)
        r = SolveMethod.get_offset_from_start(li1, [-1, -1, 1, 1, -1, -1], True)
        self.assertEqual(r, 1)

    #
    # fill line
    #
    def test_fill_when_input_line_is_empty(self):
        li1 = LayoutIndex(1)
        li2 = LayoutIndex(2)
        r = SolveMethod.fill_line([li1, li2], [-1, -1, -1, -1, -1, -1], 1)

        self.assertEqual(r, [li1, (li1, li2), li2, li2, None, None])

    def test_fill_when_layout_need_more_than_nessasary(self):
        li1 = LayoutIndex(2)
        li2 = LayoutIndex(3)

        self.assertRaises(LineOutOfRange, SolveMethod.fill_line, [li1, li2], [-1, -1, -1, -1, -1], 1)

    def test_fill_full_line_1(self):
        li1 = LayoutIndex(2)
        li2 = LayoutIndex(1)
        r = SolveMethod.fill_line([li1, li2], [-1, -1, -1, -1], 1)

        self.assertEqual(r, [li1, li1, (li1, li2), li2])

    def test_fill_full_line_2(self):
        li1 = LayoutIndex(2)
        r = SolveMethod.fill_line([li1], [-1, -1, 0, -1], 1)

        self.assertEqual(r, [li1, li1, (li1, None), (li1, None)])

    def test_fill_full_line_3(self):
        li1 = LayoutIndex(2)
        r = SolveMethod.fill_line([li1], [-1, 0, -1, -1], 1)

        self.assertEqual(r, [(li1, None), (li1, None), li1, li1])

    def test_fill_full_line_4(self):
        r = SolveMethod.fill_line([], [-1, -1, -1, -1], 1)
        self.assertEqual(r, [(None, None)]*4)

    def test_fill_full_line_5(self):
        li1 = LayoutIndex(2)
        r = SolveMethod.fill_line([li1], [-1, -1, 1, -1], 1)

        self.assertEqual(r, [(li1, None), li1, li1, None])

    def test_fill_full_line_6(self):
        li1 = LayoutIndex(3)
        r = SolveMethod.fill_line([li1], [-1, 1, 1, 1], 1)

        self.assertEqual(r, [(li1, None), li1, li1, li1])

    def test_fill_full_line_7(self):
        li1 = LayoutIndex(4)
        r = SolveMethod.fill_line([li1], [-1, -1, -1, -1, -1, -1, -1, 1, -1], 1)

        self.assertEqual(r, [(li1, None), (li1, None), (li1, None), (li1, None), li1, li1, li1, li1, None])

    def test_fill_full_line_8(self):
        li1 = LayoutIndex(4)
        r = SolveMethod.fill_line([li1], [-1, 1, -1, -1, -1, -1, -1, -1, -1], 1)

        self.assertEqual(r, [li1, li1, li1, li1, None, (li1, None), (li1, None), (li1, None), (li1, None)])

    def test_fill_full_line_9(self):
        li1 = LayoutIndex(1)
        li2= LayoutIndex(1)
        r = SolveMethod.fill_line([li1, li2], [-1, -1, -1, -1, 1, -1, -1, 1, -1], 1)

        self.assertEqual(r, [(li1, None), (li1, None), (li1, None), (li1, None), li1, (li1, li2), (li1, li2), li2, (li2, None)])

    def test_fill_full_line_10(self):
        li1 = LayoutIndex(1)
        r = SolveMethod.fill_line([li1], [-1, 1, -1], 1)

        self.assertEqual(r, [(li1, None), li1, (li1, None)])

    #
    # find intersection
    #
    def test_find_intersection_x5_l3(self):
        li1 = LayoutIndex(3)
        r = SolveMethod.find_intersection([li1], [-1, -1, -1, -1, -1], 1)

        self.assertEqual(r, [None, None, 1, None, None])

    def test_find_intersection_x4_l2(self):
        li1 = LayoutIndex(2)
        r = SolveMethod.find_intersection([li1], [-1, -1, -1, -1], 1)

        self.assertEqual(r, [None, None, None, None])

    def test_find_intersection_x4_l2_with_dot(self):
        li1 = LayoutIndex(2)
        r = SolveMethod.find_intersection([li1], [-1, -1, 0, -1], 1)

        self.assertEqual(r, [1, 1, 0, 0])

    def test_find_intersection_x4_l2a1(self):
        li1 = LayoutIndex(2)
        li2 = LayoutIndex(1)
        r = SolveMethod.find_intersection([li1, li2], [-1, -1, -1, -1], 1)

        self.assertEqual(r, [1, 1, 0, 1])

    def test_find_intersection_x13_l1_7_1(self):
        li1 = LayoutIndex(1)
        li2 = LayoutIndex(7)
        li3 = LayoutIndex(1)
        r = SolveMethod.find_intersection([li1, li2, li3], [-1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1], 1)

        self.assertEqual(r, [None, None, None, None, 1, 1, 1, 1, 1, None, None, None, None])

    def test_find_intersection_x5_l3_already_full(self):
        li1 = LayoutIndex(3)
        r = SolveMethod.find_intersection([li1], [-1, 1, 1, 1, -1], 1)

        self.assertEqual(r, [0, 1, 1, 1, 0])

    def test_find_intersection_x13_l2_1_1_2(self):
        li1 = LayoutIndex(2)
        li2 = LayoutIndex(1)
        li3 = LayoutIndex(1)
        li4 = LayoutIndex(2)
        r = SolveMethod.find_intersection([li1, li2, li3, li4], [0, 0, -1, 1, 0, -1, 0, -1, 0, 1, -1, 0, 0], 1)

        self.assertEqual(r, [0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0])

    def test_find_intersection_x5_l2(self):
        li1 = LayoutIndex(2)
        r = SolveMethod.find_intersection([li1], [-1]*5, 1)

        self.assertEqual(r, [None]*5)

    def test_find_intersection_x10_l4(self):
        li1 = LayoutIndex(4)
        r = SolveMethod.find_intersection([li1], [-1, 1, 1, 1, -1, -1, -1, -1, -1, -1], 1)

        self.assertEqual(r, [None, 1, 1, 1, None, 0, 0, 0, 0, 0])

    def test_find_intersection_x10_l4(self):
        li1 = LayoutIndex(2)
        li2 = LayoutIndex(1)
        r = SolveMethod.find_intersection([li1, li2], [1, -1, -1, 1, -1], 1)

        self.assertEqual(r, [1, 1, 0, 1, 0])

    def test_find_intersection_x10_l4(self):
        li1 = LayoutIndex(2)
        li2 = LayoutIndex(1)
        r = SolveMethod.find_intersection([li1, li2], [1, -1, -1, 1, -1], 1)

        self.assertEqual(r, [1, 1, 0, 1, 0])

    def test_find_intersection_x6_l1_1(self):
        li1 = LayoutIndex(1)
        li2 = LayoutIndex(1)
        r = SolveMethod.find_intersection([li1, li2], [-1, 1, -1, -1, 1, -1], 1)

        self.assertEqual(r, [0, 1, 0, 0, 1, 0])

if __name__ == '__main__':
    unittest.main()