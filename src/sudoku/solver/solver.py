from copy import copy, deepcopy

from sudoku.solution import Solution
from probability_policy import CheckProbabilityLinePolicy

class SudokuSolverException(RuntimeError):
    pass

class Solver(object):
    def __init__(self):
        self.policies = [CheckProbabilityLinePolicy()]

    def solve(self, descr):
        self.solution = Solution(descr)

        l1, l2 = 0, None
        while l1 != l2:
            l1 = len(self.solution.steps)
            for p in self.policies:
                p.solve(self.solution)

            l2 = len(self.solution.steps)

        return self.solution
