import json
import numpy
from collections import OrderedDict
from copy import deepcopy

class Value(object):
    def __init__(self, value):
        self.v = value

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


class Matrix(object):
    def __init__(self, matrix=None, x=None, y=None, default=None):
        if matrix:
            y = len(matrix)
            assert y > 0
            x = len(matrix[0])

            self.data = [[Value(matrix[j][i]) for i in xrange(x)] for j in xrange(y)]
        else:
            self.data = [[Value(default) for i in xrange(x)] for i in xrange(y)]

        self.shape = (x, y)

    @staticmethod
    def from_shape(x, y, default=None):
        return Matrix(x=x, y=y, default=default)

    @staticmethod
    def from_matrix(matrix):
        return Matrix(matrix=matrix)

    def __eq__(self, other):
        if type(other) is not Matrix:
            return False

        if self.shape != other.shape:
            return False

        x, y = self.shape
        for i in xrange(y):
            if self.row(i) != other.row(i):
                return False

        return True

    def row(self, i):
        assert len(self.data) >= i
        return self.data[i]

    def column(self, i):
        return [self.data[j][i] for j in xrange(len(self.data))]

    def value(self, x, y):
        return self.data[x][y].v

    def item(self, x, y):
        return self.data[x][y]

