from base.solution import Solution
from layout_index import LayoutIndex

class SolutionStep(object):
    def __init__(self, nonogram):
        self._uid = 1000
        self._idToIndex = {}
        self._nonogram = nonogram

        self._idToIndex[-1] = -1
        self._idToIndex[0] = 0

        self.row = [[self.__getIndex(x) for x in r] for r in nonogram.rows()]
        self.column = [[self.__getIndex(x) for x in c] for c in nonogram.columns()]

        y_size, x_size = self.shape()
        self._sol = Solution(shape=(x_size, y_size))


    def __getIndex(self, value):
        uid = self._uid
        self._uid = self._uid + 1
        index = LayoutIndex(value, self._uid)
        self._idToIndex[self._uid] = index

        return index

    def index(self, uid):
        return self._idToIndex[int(uid)]

    def shape(self):
        return (len(self.column), len(self.row))

    def solution(self):
        return self._sol

    def row_layout_and_solution(self, i):
        return self.row[i], self._sol.row(i)

    def col_layout_and_solution(self, i):
        return self.column[i], self._sol.col(i)