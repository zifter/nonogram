from copy import copy, deepcopy

from sudoku.solution import Solution
from probability_policy import ProbabilitySolverPolicy

class SudokuSolverException(RuntimeError):
    pass

class Solver(object):
    def __init__(self):
        self.policies = [ProbabilitySolverPolicy()]

    def solve(self, descr):
        solution = Solution(descr)
        steps = 0

        l1, l2 = 0, None
        while l1 != l2:
            l1 = len(solution.steps)
            for p in self.policies:
                p.solve(solution)

            l2 = len(solution.steps)

            steps += 1

        return solution, steps
