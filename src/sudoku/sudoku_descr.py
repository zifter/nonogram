import json
import math
from common.matrix import Matrix

class SudokuDescr(object):
    def __init__(self, matrix=None):
        self.matrix = Matrix(matrix=matrix)
        y_size = int(math.sqrt(self.matrix.shape[0]))
        x_size = int(math.sqrt(self.matrix.shape[1]))
        self._box_shape = (x_size, y_size)
        self._values = set([i + 1 for i in xrange(x_size*y_size)])

    def __eq__(self, other):
        return other is not None \
               and self.matrix == other.matrix

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return SudokuDescrPrinter.pretty_string(self)

    def values(self):
        return self._values

    def box_shape(self):
        return self._box_shape


    def save(self):
        return {"matrix", self.matrix}

    def save_to_file(self, filepath):
        with open(filepath, 'w') as outfile:
            json.dump(self.save(), outfile, indent=4, sort_keys=False)

    @staticmethod
    def load(data):
        return SudokuDescr(**data)

    @staticmethod
    def load_from_file(filepath):
        with open(filepath, "r") as inputfile:
            return SudokuDescr.load(json.load(inputfile))


class SudokuDescrPrinter():
    @staticmethod
    def pretty_string(descr):
        s = ""
        x_box_size, y_box_size = descr.box_shape()
        x_size, y_size = descr.matrix.shape
        for y in xrange(y_size):
            if y % y_box_size == 0 and y > 0:
                s += '-'*(y_size + y_size/x_box_size) + '\n'

            for x in xrange(x_size):
                v = descr.matrix.value(x, y)
                if v != 0:
                    s += str(v)
                else:
                    s += "."

                if (x + 1) % x_box_size == 0:
                    s += '|'

            s += '\n'

        return s

