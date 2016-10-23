import json

from collections import OrderedDict

from sudoku.sudoku_descr import SudokuDescr
from common.matrix import Matrix, Value


class _CustomEncoder(SudokuDescr):
    """
    JSONEncoder subclass that leverages an object's `__json__()` method,
    if available, to obtain its default JSON representation.

    """
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__(self)
        return json.JSONEncoder.default(self, obj)


class Solution(SudokuDescr):
    def __init__(self, descr=None):
        SudokuDescr.__init__(self, matrix=descr.matrix)
        self.steps = []  # ((x, y), value)
        x, y = descr.matrix.shape

    def values(self):
        return set([1, 2, 3, 4, 5, 6, 7, 8, 9])

    def add_step(self, index, value):
        self.steps.append((index, value))
        self.matrix.item_i(index).v = value
