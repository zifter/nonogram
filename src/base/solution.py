import json

from collections import OrderedDict
from matrix import Matrix

class _CustomEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that leverages an object's `__json__()` method,
    if available, to obtain its default JSON representation.

    """
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__(self)
        return json.JSONEncoder.default(self, obj)

class Solution(object):
    def __init__(self, matrix=[], shape=None):
        if shape:
            x, y = shape
            self.matrix = Matrix.from_shape(x=x, y=y, default=-1)
        else:
            self.matrix = Matrix.from_matrix(matrix)

    def __eq__(self, other):
        return other is not None \
               and self.matrix == other.matrix

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return SolutionPrinter.pretty_string(self)

    def shape(self):
        return self.matrix.shape

    def item(self, x, y):
        return self.matrix.item(x, y)

    def value(self, x, y):
        return self.item(x, y).v

    def col(self, index):
        return self.matrix.column(index)

    def row(self, index):
        return self.matrix.row(index)

    @staticmethod
    def load(data):
        return Solution(**data)

    @staticmethod
    def load_from_file(filepath):
        with open(filepath, "r") as inputfile:
            return Solution.load(json.load(inputfile))

    def save(self):
        return OrderedDict([("matrix", self.matrix.data)])

    def save_to_file(self, filepath):
        with open(filepath, 'w') as outfile:
            json.dump(self.save(), outfile, indent=4, sort_keys=False, cls=_CustomEncoder)


class SolutionPrinter():
    @staticmethod
    def pretty_string(solution, selected_row=None, selected_column=None):
        s = ""
        x_size, y_size = solution.shape()
        if not x_size or not y_size:
            return "|e|"

        for i in xrange(y_size):
            delimiter = '|'
            if i == selected_row:
                delimiter = '\\'

            s += delimiter
            for j in xrange(x_size):
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

