from solution_step import SolutionStep

from copy import copy, deepcopy

class SolverException(RuntimeError):
    pass

class LineOutOfRange(SolverException):
    pass

class Solver(object):
    def __init__(self):
        self.type = "black"
        self.nonogram = None
        self.ss = None

    def solve(self, nonogram):
        self.nonogram = nonogram

        ss = SolutionStep(self.nonogram)
        self.ss = ss

        self.execute_for_each_line(self.find_intersection)

        self.ss = None
        return ss.solution()

    def execute_for_each_line(self, func):
        x_size, y_size = self.ss.shape()
        space = self.nonogram.space_size()
        for i in xrange(y_size):
            layout, line = self.ss.row_layout_and_solution(i)
            func(layout, line, space)

        for i in xrange(x_size):
            layout, line = self.ss.col_layout_and_solution(i)
            func(layout, line, space)

    def find_intersection(self, layout, line, space):
        result_line = SolveMethod.find_intersection(layout, [self.ss.index(l) for l in line], space)
        for i in xrange(len(result_line)):
            if result_line[i]:
                line[i] = result_line[i]


class SolveMethod(object):
    @staticmethod
    def make_space(index1, index2):
        if index1:
            if index2:
                if index1.id() == index2.id():
                    raise SolverException()

                if index1.id() < index2.id():
                    return (index1, index2)
                else:
                    return (index2, index1)
            else:
                return (index1, None)
        else:
            if not index2:
                raise SolverException()

            return (index2, None)

    @staticmethod
    def fill_line(layout, line, space):
        """

        :param layout: [LayoutIndex, ..]
        :param line:  [0, 0, 0, 1, ]. 0 - undefined, value > 0 - it's a index of layout index
        :param space: size of space
        :return: [LayoutIndex] suitable line for this layout
        """
        result = deepcopy(line)
        s = 0
        for i in xrange(len(layout)):
            index = layout[i]
            next_index = layout[i + 1] if len(layout) > (i + 1) else None

            for v in xrange(index.value()):
                if s >= len(result):
                    raise LineOutOfRange()

                result[s] = index
                s += 1

            space = space if next_index is not None else len(result) - s
            for v in xrange(space):
                if next_index is not None and s >= len(result):
                    raise LineOutOfRange()

                result[s] = SolveMethod.make_space(index, next_index)
                s += 1

        return result

    @staticmethod
    def find_intersection(layout, line, space):
        forward_line = SolveMethod.fill_line(layout, line, space)
        reversed_line = SolveMethod.fill_line(list(reversed(layout)), line, space)[::-1]

        result = [None] * len(line)
        for i in xrange(len(line)):
            if forward_line[i] == reversed_line[i]:
                # -1 - space
                result[i] = 0 if type(forward_line[i]) is tuple else reversed_line[i].id()

        return result
