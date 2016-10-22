from nonogram.base.solution import Solution
from nonogram.base.matrix import Matrix
from nonogram.solver.layout_index import LayoutIndex, SolutionCell

class SolutionStep(object):
    ROW = 0
    COL = 1
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
        self.matrix = Matrix(x=x_size, y=y_size, default=SolutionCell())

    def __getIndex(self, value):
        self._uid = self._uid + 1
        index = LayoutIndex(value)
        self._idToIndex[index.id()] = index

        return index

    def index(self, uid):
        return self._idToIndex[int(uid)]

    def shape(self):
        return (len(self.column), len(self.row))

    def solution(self):
        return self._sol

    def row_layout(self, i):
        return self.row[i]

    def column_layout(self, i):
        return self.column[i]

    def row_lineup(self, i):
        return [x.v[self.ROW] for x in self.matrix.row(i)]

    def col_lineup(self, i):
        return [x.v[self.COL] for x in self.matrix.column(i)]

    def set_row(self, i, j, item):
        self.matrix.row(i)[j][self.ROW] = item
        self._sol.item(i, j).v = item.color()

    def set_col(self, i, j, item):
        self.matrix.col(i)[self.COL] = item
        self._sol.item(j, i).v = item.color()