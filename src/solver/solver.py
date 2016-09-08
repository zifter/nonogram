from solution_step import SolutionStep

from copy import copy, deepcopy

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
        proxy = self.__fill_line(layout, line, space)
        rproxy = self.__fill_line(reversed(layout), line, space)[::-1]

        a = 0
        for i in xrange(len(line)):
            if proxy[i] is not None and proxy[i] == rproxy[i]:
                line[i] = proxy[i].id()

    def __fill_line(self, layout, line, space):
        proxy = []
        for l in line:
            proxy.append(self.ss.index(l))

        s = 0
        for index in layout:
            for v in xrange(index.value()):
                proxy[s] = index
                s = s + 1

            s = s + space

        return proxy
