from copy import copy, deepcopy

import unittest

from test_sudoku.testcase_sudoku import TestCaseSudoku
from sudoku.solver.solver import Solver
from sudoku.solution import Solution
from sudoku.solution import SudokuDescr
import cProfile

# https://habrahabr.ru/post/173795/

def profile(func):
    """Decorator for run function profile"""
    def wrapper(*args, **kwargs):
        profile_filename = func.__name__ + '.prof'
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.print_stats(sort="cumtime")
        return result
    return wrapper

class TestSolver(TestCaseSudoku):
    #@profile
    def test_solve_and_compare(self):
        test_data = self.getSolverData()
        mySolver = Solver()

        for name, layout, solution in test_data:
            print "# ------ SUDOKU: %s ------- #" % name
            d0 = SudokuDescr.load_from_file(layout)
            print d0

            s1, steps = mySolver.solve(d0)
            print "steps: %s " % steps
            print s1

            s0 = Solution.load_from_file(solution)
            print "answer"
            print s0

            self.assertEqual(s0, s1, "Solution failed: %s" % solution)


if __name__ == '__main__':
    unittest.main()