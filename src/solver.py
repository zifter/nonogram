from nonogram import Nonogram, Solution

class Solver(object):
    def __init__(self):
        self.type = "black"
        self.nonogram = None
        self.sol = None

    def solve(self, nonogram):
        self.nonogram = nonogram

        sol = Solution(shape=self.nonogram.shape())
        self.sol = sol

        self.execute_for_each_line(self.find_intersection)

        self.sol = None
        return sol

    def execute_for_each_line(self, func):
        x, y = self.nonogram.shape()
        for i in xrange(x):
            row = self.nonogram.row_layout(i)
            func(row, self.sol.row(i))

        for i in xrange(y):
            col = self.nonogram.col_layout(i)
            func(col, self.sol.col(i))

    def find_intersection(self, layout, line):
        print layout, line