import json
import numpy
from collections import OrderedDict

class Solution(object):
    def __init__(self, matrix=[], shape=None):
        if shape:
            self.matrix = numpy.matrix(numpy.empty(shape=shape))
            self.matrix.fill(-1) # undefined
        else:
            self.matrix = numpy.matrix(matrix)

    def __eq__(self, other):
        return other is not None \
               and numpy.array_equal(self.matrix, other.matrix)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return SolutionPrinter.pretty_string(self)

    def shape(self):
        return self.matrix.shape

    def value(self, x, y):
        return self.matrix[x, y]

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
        return OrderedDict([("matrix", self.matrix.tolist())])

    def save_to_file(self, filepath):
        with open(filepath, 'w') as outfile:
            json.dump(self.save(), outfile, indent=4, sort_keys=False)


class SolutionPrinter():
    @staticmethod
    def pretty_string(solution, selected_row=None, selected_column=None):
        s = ""
        x_size, y_size = solution.shape()
        if not x_size or not y_size:
            return "|e|"

        for i in xrange(x_size):
            delimiter = '|'
            if i == selected_row:
                delimiter = '\\'

            s += delimiter
            for j in xrange(y_size):
                if solution.value(i, j) > 0:
                    s += '#'
                elif solution.value(i, j) == 0:
                    s += ' '
                else:
                    s += '?'

                delimiter = '|'
                if i == selected_row:
                    delimiter = '\\'
                elif (j + 1) == selected_column:
                    delimiter = '>'

                s += delimiter

            s += '\n'

        return s

