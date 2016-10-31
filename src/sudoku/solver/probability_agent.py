from copy import copy
from sudoku.solver.solver_method import SolverPolicy


class RamdomChoiceAgent(SolverPolicy):
    def __init__(self):
        SolverPolicy.__init__(self)

    def solve(self, solution):
        p = []
        for i in solution.probability:
            if not i.v.isReady():
                p.append(i)

        if not p:
            return False

        p.sort(key=lambda v: len(v.v.values()))
        item = p[0]
        solution.add_random_choice(item.index(), item.v.values())

        return True


class ProbabilitySolverAgent(SolverPolicy):
    def __init__(self):
        SolverPolicy.__init__(self)
        self.strategy = [FindUniquePossibleValueInBelongedLineStrategy()]

    def solve(self, solution):
        found = False
        for p in self.strategy:
            for item in solution.probability:
                if not item.v.isReady():
                    v = p.find(solution, item)
                    if v:
                        solution.add_step(item.index(), v)
                        found = True

        return found

# ---------------------------------
class FindValueStrategy():
    def find(self, solution, item):
         raise NotImplemented()


class FindUniquePossibleValueInBelongedLineStrategy(FindValueStrategy):
    def find(self, solution, item):
        lines = solution.probability_line(item.index())
        for l in lines:
            line_p = item.v.values()
            for i in l:
                if item != i:
                    line_p = line_p - i.v.values()

            if len(line_p) == 1:
                return line_p.pop()

        return None