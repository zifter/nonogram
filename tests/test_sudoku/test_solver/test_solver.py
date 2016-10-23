from copy import copy, deepcopy

import unittest

from test_sudoku.testcase_sudoku import TestCaseSudoku
from sudoku.solver.solver import Solver
from sudoku.solution import Solution
from sudoku.solution import SudokuDescr

class TestSolver(TestCaseSudoku):
    def test_solve_and_compare(self):
        test_data = self.getSolverData()
        mySolver = Solver()

        for layout, solution in test_data:
            print "# ------ SUDOKU ------- #"
            d0 = SudokuDescr.load_from_file(layout)
            print d0

            print "# ------ SOLUTION ------- #"
            s1 = mySolver.solve(d0)
            print s1

            print "# ------ ANSWER ------- #"
            s0 = Solution.load_from_file(solution)
            print s0

            self.assertEqual(s0, s1, "Solution failed: %s" % solution)
            print "# ------ END ------- #"


if __name__ == '__main__':
    unittest.main()