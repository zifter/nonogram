import env

import unittest

from tests.testcase_based_on_data import TestCaseBasedOnData

from nonogram import Nonogram, Solution
from solver import Solver

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

if __name__ == '__main__':
    unittest.main()