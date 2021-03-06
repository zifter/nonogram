import json
import numpy

import math
from collections import Iterator
from copy import deepcopy

class Value(object):
    def __init__(self, value, x, y):
        self.v = value
        self.idx = (x, y)

    def __eq__(self, other):
        return (type(other) is Value and self.v == other.v) \
               or self.v == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.v)

    def __repr__(self):
        return "v<%s>" % str(self.v)

    def __json__(self, encoder):
        return self.v

    def index(self):
        return self.idx


class MatrixIterator(Iterator):
    def __init__(self, matrix):
        self.m = matrix
        self.i = 0

    def next(self):
        try:
            x, y = self.m.shape
            if self.i >= (x * y):
                raise StopIteration

            return self.m.item(self.i % x, int(math.floor(self.i / y)))
        finally:
            self.i += 1


class Matrix(object):
    @staticmethod
    def from_shape(x, y, default=None):
        return Matrix(x=x, y=y, default=default)

    @staticmethod
    def from_matrix(matrix):
        return Matrix(matrix=matrix)

    def __init__(self, matrix=None, x=None, y=None, default_func=lambda _1, _2: None):
        if matrix and type(matrix) is Matrix:
            self.shape = matrix.shape
            self.data = deepcopy(matrix.data)
        elif matrix:
            y = len(matrix)
            assert y > 0
            x = len(matrix[0])

            self.shape = (x, y)
            self.data = [[Value(matrix[j][i], i, j) for i in xrange(x)] for j in xrange(y)]
        else:
            self.shape = (x, y)
            self.data = [[Value(default_func(i, j), i, j) for i in xrange(x)] for j in xrange(y)]

    def __eq__(self, other):
        if type(other) is not Matrix:
            return False

        if self.shape != other.shape:
            return False

        return self.data == other.data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iter__(self):
        return MatrixIterator(self)

    def reset(self, default_func):
        x, y = self.shape
        for i in xrange(y):
            for j in xrange(x):
                self.data[i][j].v = default_func(i, j)

    def sub_matrix(self, x, y, shape):
        m = Matrix(x=shape[0], y=shape[1])
        for j in xrange(shape[1]):
            for i in xrange(shape[0]):
                m.set_item(i, j, self.item(x + i, y + j))

        return m

    def to_list(self):
        r = []
        for row in self.data:
            r += row
        return r

    def row(self, i):
        assert len(self.data) >= i
        return self.data[i]

    def column(self, i):
        return [self.data[j][i] for j in xrange(len(self.data))]

    def value_i(self, index):
        x, y = index
        return self.data[y][x].v

    def value(self, x, y):
        return self.data[y][x].v

    def item_i(self, index):
        x, y = index
        return self.data[y][x]

    def item(self, x, y):
        return self.data[y][x]

    def set_item(self, x, y, item):
        self.data[y][x] = item