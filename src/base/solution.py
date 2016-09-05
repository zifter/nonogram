import json
import numpy
from collections import OrderedDict

class Nonogram(object):
    def __init__(self, type="black", row=[], column=[]):
        self.type = type
        self._row = row
        self._column = column

    def __eq__(self, other):
        return other is not None \
               and self.type == other.type \
               and numpy.array_equal(self._row, other._row) \
               and numpy.array_equal(self._column, other._column)

    def __ne__(self, other):
        return not self.__eq__(other)

    def shape(self):
        return (len(self._row), len(self._column))

    def row_layout(self, i):
        return self._row[i]

    def col_layout(self, i):
        return self._column[i]

    @staticmethod
    def load(data):
        return Nonogram(**data)

    @staticmethod
    def load_from_file(filepath):
        with open(filepath, "r") as inputfile:
            return Nonogram.load(json.load(inputfile))

    def save(self):
        return OrderedDict([("type", self.type), ("row", self._row), ("column", self._column)])

    def save_to_file(self, filepath):
        with open(filepath, 'w') as outfile:
            json.dump(self.save(), outfile, indent=4, sort_keys=False)



class Solution(object):
    def __init__(self, matrix=[], shape=None):
        if shape:
            self.matrix = numpy.matrix(numpy.zeros(shape=shape))
        else:
            self.matrix = numpy.matrix(matrix)
            self.matrix = self.matrix.transpose()

    def __eq__(self, other):
        return other is not None \
               and numpy.array_equal(self.matrix, other.matrix)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        s = ""
        x, y = self.matrix.shape
        if not x or not y:
            return "|e|"

        for j in xrange(y):
            s += '|'
            for i in xrange(x):
                s += '#|' if self.matrix[i, j] else ' |'
            s += '\n'

        return s

    def is_valid(self):
        valid = True

        return valid

    def col(self, index):
        return self.matrix.A[:, index]

    def row(self, index):
        return self.matrix.A[index,:]

    @staticmethod
    def load(data):
        return Solution(**data)

    @staticmethod
    def load_from_file(filepath):
        with open(filepath, "r") as inputfile:
            return Solution.load(json.load(inputfile))

    def save(self):
        return OrderedDict([("matrix", self.matrix.transpose().tolist())])

    def save_to_file(self, filepath):
        with open(filepath, 'w') as outfile:
            json.dump(self.save(), outfile, indent=4, sort_keys=False)
