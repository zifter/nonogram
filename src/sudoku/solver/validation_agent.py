from copy import copy, deepcopy

from common.matrix import Matrix
from sudoku.solver.iterator import IteratorLine, IteratorBoxToList
from sudoku.solver.solver_method import SolverMethod, SolverPolicy


class ValidationSolverAgent(SolverPolicy):
    def __init__(self):
        SolverPolicy.__init__(self)

    def solve(self, solution):
        for it in [IteratorLine(solution.matrix), IteratorBoxToList(solution.matrix, solution.box_shape())]:
            v = it.next()
            while v:
                if not self.is_line_valid(v):
                    solution.rollback_random()
                    return True

                v = it.next()

        return False


    def is_line_valid(self, line):
        v = []
        for x in line:
            if x.v:
                v.append(x.v)
        return len(v) == len(set(v))