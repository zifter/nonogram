from sudoku.sudoku_descr import SudokuDescr


class Solution(SudokuDescr):
    def __init__(self, descr=None):
        SudokuDescr.__init__(self, matrix=descr.matrix)
        self.steps = []  # ((x, y), value)

    def add_step(self, index, value):
        self.steps.append((index, value))
        self.matrix.item_i(index).v = value
