from copy import copy, deepcopy

from common.matrix import Matrix
from sudoku.solver.iterator import IteratorLine, IteratorBoxToList
from sudoku.solver.solver_method import SolverMethod, SolverPolicy


class ProbabilitySolverPolicy(SolverPolicy):
    class Probability(object):
        def __init__(self):
            self.poss = set()
            self.imposs = set()

        def possible_values(self):
            return self.poss - self.imposs

        def __repr__(self):
            return str(self.possible_values())

        def __str__(self):
            return str(self.possible_values())


    def __init__(self):
        SolverPolicy.__init__(self)
        self.probability_agent = [FindLineProbabilityAgent(), FindBoxProbabilityAgent()]
        self.value_agent = [FindWithOnePossibleValueAgent(), FindUniquePossibleValueInBelongedLineAgent()]

    def solve(self, solution):
        x, y = solution.matrix.shape
        probability = Matrix(x=x, y=y, default_func=lambda _1, _2: ProbabilitySolverPolicy.Probability())

        for p in self.probability_agent:
            p.find(solution, probability)

        for item in probability:
            for agent in self.value_agent:
                v = agent.find(solution, probability, item)
                if v:
                    solution.add_step(item.index(), v)


# ---------------------------------
class FindProbabilityAgent(object):
    def find(self, solution, probability):
        raise NotImplemented()


class FindLineProbabilityAgent(FindProbabilityAgent):
    def get_iterator(self, solution):
        return IteratorLine(solution.matrix)

    def find(self, solution, probability):
        it = self.get_iterator(solution)

        v = it.next()
        while v:
            defined, undefined = SolverMethod.line_layout(v)

            not_needs = set([i.v for i in defined])
            needs = solution.values() - not_needs

            for i in undefined:
                p = probability.value_i(i.index())
                p.poss.update(needs)
                p.imposs.update(not_needs)

            v = it.next()


class FindBoxProbabilityAgent(FindLineProbabilityAgent):
    def get_iterator(self, solution):
        return IteratorBoxToList(solution.matrix, solution.box_shape())


# ---------------------------------
class FindValueAgent():
    def find(self, solution, probability, item):
         raise NotImplemented()


class FindWithOnePossibleValueAgent():
    def find(self, solution, probability, item):
        p = item.v.possible_values()
        if len(p) == 1:
            return p.pop()

        return None


class FindUniquePossibleValueInBelongedLineAgent(FindValueAgent):
    def find(self, solution, probability, item):
        p = item.v.possible_values()
        x, y = item.index()
        rl = probability.row(y)
        cl = probability.column(x)
        bl = SolverMethod.belonged_box(x, y, probability, solution.box_shape()).to_list()

        for l in [rl, cl, bl]:
            line_p = copy(p)
            for i in l:
                if item != i:
                    line_p = line_p - i.v.possible_values()

            if len(line_p) == 1:
                return line_p.pop()

        return None