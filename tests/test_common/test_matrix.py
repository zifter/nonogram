import env

import unittest

from test_nonogram.testcase_nonogram import TestCaseNonogram
from common.matrix import Matrix

#--------------------------------------------------------------------------
class TestMatrixClass(TestCaseNonogram):
    def test_ctor(self):
        m = Matrix.from_shape(3, 5)

        for i in xrange(5):
            self.assertEqual(m.row(i), 3*[None])

        for i in xrange(3):
            self.assertEqual(m.column(i), 5*[None])

    def test_change_value_in_row(self):
        m = Matrix.from_shape(3, 5)

        value = "new_value"
        m.row(1)[2].value = value
        self.assertEqual(m.column(2)[1].value, value)


    def test_change_value_in_column(self):
        m = Matrix.from_shape(3, 5)

        value = "new_value"
        m.column(1)[2].value = value
        self.assertEqual(m.row(2)[1].value, value)

    def test_create_from_matrix(self):
        m = Matrix.from_matrix([
            [1, 2],
            [3, 4],
            [5, 6],
        ])

        self.assertEqual(m.row(0), [1, 2])
        self.assertEqual(m.row(1), [3, 4])
        self.assertEqual(m.row(2), [5, 6])

        self.assertEqual(m.column(0), [1, 3, 5])
        self.assertEqual(m.column(1), [2, 4, 6])

if __name__ == '__main__':
    unittest.main()