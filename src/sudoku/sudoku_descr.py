import json

from common.matrix import Matrix

class SudokuDescr(object):
    def __init__(self, matrix=None):
        self.matrix = Matrix(matrix=matrix)

    def __eq__(self, other):
        return other is not None \
               and self.matrix == other.matrix

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return SudokuDescrPrinter.pretty_string(self)

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
        x_size, y_size = descr.matrix.shape
        for y in xrange(y_size):
            if y % 3 == 0 and y > 0:
                s += '-'*(y_size*4/3) + '\n'

            for x in xrange(x_size):
                v = descr.matrix.value(x, y)
                if v != 0:
                    s += str(v)
                else:
                    s += "."

                if (x + 1) % 3 == 0:
                    s += '|'

            s += '\n'

        return s

