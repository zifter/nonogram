import env

import unittest

from test_nonogram.nonogram_testcase import TestNonogram

from nonogram.base.nonogram_obj import Nonogram
from nonogram.solver.solution_step import SolutionStep

class TestSolutionStep(TestNonogram):
    def test_from_nonogram(self):
        n0 = Nonogram("black", [[1], [2], [3, 4]], [[1, 3], [2, 5]])
        ss0 = SolutionStep(n0)

        self.assertEqual(n0.shape(), ss0.shape())

        x_size, y_size = n0.shape()

        for i in xrange(y_size):
            rl = n0.row_layout(i)
            for j in xrange(len(rl)):
                self.assertEqual(ss0.row[i][j].value(), rl[j])

        for i in xrange(x_size):
            cl = n0.col_layout(i)
            for j in xrange(len(cl)):
                self.assertEqual(ss0.column[i][j].value(), cl[j])

    def test_all_indexes_is_unique(self):
        n0 = Nonogram("black", [[1], [2], [3, 4]], [[1, 3], [2, 5]])
        ss0 = SolutionStep(n0)

        x_size, y_size = n0.shape()
        indexes = 0
        ids = set()

        for i in xrange(y_size):
            rl = n0.row_layout(i)
            for j in xrange(len(rl)):
                indexes = indexes + 1
                ids.add(ss0.row[i][j])

        for i in xrange(x_size):
            cl = n0.col_layout(i)
            for j in xrange(len(cl)):
                indexes = indexes + 1
                ids.add(ss0.column[i][j])

        self.assertEqual(len(ids), indexes)

    def test_get_layout_and_solution_line(self):
        n0 = Nonogram("black", [[1], [2], [3, 4]], [[1, 3], [2, 5]])
        ss0 = SolutionStep(n0)

        x, y = ss0.shape()

        for i in xrange(x):
            l, s = ss0.row_layout(i), ss0.row_lineup(i)
            rl = n0.row_layout(i)

            for j in xrange(len(rl)):
                self.assertEqual(l[j].value(), rl[j])


if __name__ == '__main__':
    unittest.main()