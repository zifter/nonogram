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

    # return x_size, y_size
    def shape(self):
        return (len(self._column), len(self._row), )

    def row_layout(self, i):
        return self._row[i]

    def col_layout(self, i):
        return self._column[i]

    def rows(self):
        return self._row

    def columns(self):
        return self._column

    def space_size(self):
        return int(self.type == "black")

    def save(self):
        return OrderedDict([("type", self.type), ("row", self._row), ("column", self._column)])

    def save_to_file(self, filepath):
        with open(filepath, 'w') as outfile:
            json.dump(self.save(), outfile, indent=4, sort_keys=False)

    @staticmethod
    def load(data):
        return Nonogram(**data)


    @staticmethod
    def load_from_file(filepath):
        with open(filepath, "r") as inputfile:
            return Nonogram.load(json.load(inputfile))
