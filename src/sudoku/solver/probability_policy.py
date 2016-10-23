from copy import copy, deepcopy

from common.matrix import Matrix
from sudoku.solver.iterator import IteratorLine, Iterator3x3
from sudoku.solver.solver_method import SolverMethod, SolverPolicy


class CheckProbabilityLinePolicy(SolverPolicy):
    class Probability(object):
        def __init__(self):
            self.poss = set()
            self.imposs = set()

        def possible_values(self):
            return self.poss - self.imposs

    def __init__(self):
        SolverPolicy.__init__(self)
        self.policies = [CheckLine_ProbabilityPolicy(), Check3x3_ProbabilityPolicy()]

    def solve(self, solution):
        x, y = solution.matrix.shape
        probability = Matrix(x=x, y=y, default_func=lambda _1, _2: CheckProbabilityLinePolicy.Probability())

        for p in self.policies:
            p.check(solution, probability)

        for item in probability:
            p = item.v.possible_values()
            if len(p) == 1:
                solution.add_step(item.index(), p.pop())


class CheckProbabilityPolicy(object):
    def check(self, solution, probability):
        raise NotImplemented()


class CheckLine_ProbabilityPolicy(CheckProbabilityPolicy):
    def get_iterator(self, matrix):
        return IteratorLine(matrix)

    def check(self, solution, probability):
        it = self.get_iterator(solution.matrix)

        v = it.next()
        while v:
            defined, undefined = SolverMethod.line_layout(v)

            not_needs = set([i.v for i in defined])
            needs = solution.values() - not_needs
            assert len(needs) == len(undefined)

            for i in undefined:
                p = probability.value_i(i.index())
                p.poss.update(needs)
                p.imposs.update(not_needs)

            v = it.next()


class Check3x3_ProbabilityPolicy(CheckLine_ProbabilityPolicy):
    def get_iterator(self, matrix):
        return Iterator3x3(matrix)
