from copy import copy, deepcopy

from sudoku.solution import Solution
from probability_policy import ProbabilitySolverPolicy
from validation_policy import ValidationSolverPolicy

class SudokuSolverException(RuntimeError):
    pass

class Solver(object):
    class Context():
        def __init__(self, descr):
            self.solutions = [Solution(descr)]
            self.iteration = 0
            self.haveChanged = True

        def add_step(self, solution, index, value):
            solution.add_step(index, value)
            self.haveChanged = True

        def add_solution(self, solution):
            self.solutions.append(solution)

        def remove_solution(self, solution):
            self.solutions.remove(solution)


    def __init__(self):
        self.policies = [ProbabilitySolverPolicy(), ValidationSolverPolicy()]

    def solve(self, descr):
        context = Solver.Context(descr)

        while context.haveChanged:
            context.haveChanged = False

            for p in self.policies:
                p.solve(context.solutions[0], context)

            context.iteration += 1

        return context.solutions[0], context.iteration
