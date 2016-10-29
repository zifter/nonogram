from copy import copy
from sudoku.sudoku_descr import SudokuDescr
from common.matrix import Matrix
from sudoku.solver.solver_method import SolverMethod

class Probability(object):
    def __init__(self, values):
        self.vs = copy(values)
        self.history = []

    def isReady(self):
        return len(self.vs) == 1

    def values(self):
        return self.vs

    def value(self):
        return next(iter(self.vs))

    def erase(self, v, rev):
        if v in self.vs:
            self.history.append((v, rev))
            self.vs.remove(v)

            return self.isReady()

        return False

    def rollback(self, rev):
        while self.history[-1][1] >= rev:
            self.vs.add(self.history[-1][0])
            self.history.pop()

    def set(self, v, rev):
        to_del = self.vs - set([v])
        for d in to_del:
            self.erase(d, rev)

    def __repr__(self):
        return str(self.vs)

    def __str__(self):
        return str(self.vs)


class Solution(SudokuDescr):
    def __init__(self, descr=None):
        SudokuDescr.__init__(self, matrix=descr.matrix)
        self.steps = []  # ((x, y), value)
        x, y = self.matrix.shape
        self.probability = Matrix(x=x, y=y, default_func=lambda ix, iy: Probability(self.values()))
        self.pending = [] # (x, y), value
        self.random = []

        indexes = set()
        for init in self.matrix:
            if init.v != 0:
                indexes.add(init.index())
                self.add_step(init.index(), init.v)

        new_pending = []
        for i in self.pending:
            if not i[0] in indexes:
                new_pending.append(i)

        self.pending = new_pending

    def probability_line(self, index):
        return [
            SolverMethod.belonged_box(index, self.probability, self.box_shape()),
            self.probability.row(index[1]),
            self.probability.column(index[0])
        ]

    def add_step(self, index, value):
        lines = self.probability_line(index)
        for l in lines:
            for i in l:
                if i.index() != index and i.v.erase(value, len(self.steps)):
                    self.add_pending(i.index(), i.v.value())

        self.probability.item_i(index).v.set(value, len(self.steps))
        self.steps.append((index, value))
        self.matrix.item_i(index).v = value

    def add_pending(self, index, value):
        self.pending.append((index, value))

    def add_random_choice(self, index, values):
        vs = copy(values)
        v = vs.pop()
        self.random.append((index,  vs, len(self.steps)))
        self.add_step(index, v)

    def rollback_random(self):
        # revert to 0 in matrix
        r = self.random.pop()
        while not r[1]:
            r = self.random.pop()

        rev = r[2]
        while rev != len(self.steps):
            s = self.steps.pop()
            self.matrix.item_i(s[0]).v = 0

        for item in self.probability:
            item.v.rollback(rev)

        self.pending = []
        self.add_random_choice(r[0], r[1])

    def process_pending(self):
        while self.pending:
            item = self.pending.pop()
            self.add_step(item[0], item[1])

    def is_done(self):
        x, y = self.matrix.shape
        return x*y == len(self.steps)
