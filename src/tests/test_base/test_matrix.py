import env

import unittest
import tempfile
import os

from base.matrix import Matrix

#--------------------------------------------------------------------------
class TestMatrixClass(unittest.TestCase):
    def test_ctor(self):
        m = Matrix(3, 5)

        for i in xrange(5):
            self.assertEqual(m.row(i), 3*[None])

        for i in xrange(3):
            self.assertEqual(m.column(i), 5*[None])

    def test_change_value_in_row(self):
        m = Matrix(3, 5)

        value = "new_value"
        m.row(1)[2].value = value
        self.assertEqual(m.column(2)[1].value, value)


    def test_change_value_in_column(self):
        m = Matrix(3, 5)

        value = "new_value"
        m.column(1)[2].value = value
        self.assertEqual(m.row(2)[1].value, value)

if __name__ == '__main__':
    unittest.main()