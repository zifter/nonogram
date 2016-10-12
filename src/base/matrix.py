import json
import numpy
from collections import OrderedDict
from copy import deepcopy

class Value(object):
    def __init__(self, value):
        self.v = value

    def __eq__(self, other):
        return (type(other) is Value and self.v == other.value) \
               or self.v == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.v)

    def __repr__(self):
        return str(self.v)

class Matrix(object):
    def __init__(self, x, y):
        self.data = [[Value(None) for i in xrange(x)] for i in xrange(y)]

    def row(self, i):
        assert len(self.data) >= i
        return self.data[i]

    def column(self, i):
        return [self.data[j][i] for j in xrange(len(self.data))]

