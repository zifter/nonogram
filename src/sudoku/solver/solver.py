from copy import copy, deepcopy

from sudoku.solution import Solution
from probability_agent import ProbabilitySolverAgent, RamdomChoiceAgent
from validation_agent import ValidationSolverAgent

class SudokuSolverException(RuntimeError):
    pass

class Solver(object):
    def __init__(self):
        self.agents = [ProbabilitySolverAgent(), ValidationSolverAgent(), RamdomChoiceAgent()]

    def solve(self, descr):
        solution = Solution(descr)
        iteration = 0

        while not solution.is_done():
            solution.process_pending()
            for p in self.agents:
                if p.solve(solution):
                    break

            iteration += 1

            #print context.iteration
            #print context.solutions[0]

        return solution, iteration
