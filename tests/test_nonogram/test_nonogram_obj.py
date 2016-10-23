import env

import unittest
import tempfile
import os

from test_nonogram.testcase_nonogram import TestCaseNonogram
from nonogram.nonogram_obj import Nonogram

#--------------------------------------------------------------------------
class TestNonogramClass(TestCaseNonogram):
    def test_equal_to(self):
        n0     = Nonogram("black", [[1], [2], [3, 4]]        , [[1, 3], [2, 5]])
        n_type = Nonogram("color", [[1], [2], [3, 4]]        , [[1, 3], [2, 5]])
        n_row1 = Nonogram("black", [[1], [2], [3, 4], [3, 4]], [[1, 3], [2, 5]])
        n_row2 = Nonogram("black", [[1], [2], [4, 3]]        , [[1, 3], [2, 5]])
        n_col1 = Nonogram("black", [[1], [2], [3, 4]]        , [[1, 3], [2, 5], [2, 5]])
        n_col2 = Nonogram("black", [[1], [2], [3, 4]]        , [[1, 3], [5, 2]])
        n1 = Nonogram("black", [[1], [2], [3, 4]], [[1, 3], [2, 5]])

        self.assertNotEqual(n0, None)
        self.assertNotEqual(n0, n_type, "Type check")
        self.assertNotEqual(n0, n_row1, "Extra row")
        self.assertNotEqual(n0, n_row2, "Value in row isn't equal")
        self.assertNotEqual(n0, n_col1, "Extra column")
        self.assertNotEqual(n0, n_col2, "Value in column isn't equal")
        self.assertEqual(n0, n0, "The same")
        self.assertEqual(n0, n1, "The same")

    def test_load(self):
        n0 = Nonogram("black", [[1], [2], [3, 4]], [[1, 3], [2, 5]])
        n1 = Nonogram.load({"type": "black", "row": [[1], [2], [3, 4]], "column": [[1, 3], [2, 5]]})

        self.assertEqual(n0, n1)

    def test_save(self):
        n0 = Nonogram("black", [[1], [2], [3, 4]], [[1, 3], [2, 5]])

        self.assertEqual(n0.save(), {"type": "black", "row": [[1], [2], [3, 4]], "column": [[1, 3], [2, 5]]})

    def test_save_and_load_using_file(self):
        handler, tmpfile = tempfile.mkstemp(prefix="nonogram_")

        try:
            n0 = Nonogram("black", [[1], [2], [3, 4]], [[1, 3], [2, 5]])
            n0.save_to_file(tmpfile)

            n1 = Nonogram.load_from_file(tmpfile)

            self.assertEqual(n0, n1)
        finally:
            os.close(handler)
            os.remove(tmpfile)

    def test_shape_layout_getter(self):
        n0 = Nonogram("black", [[1], [2], [3, 4]], [[1, 3], [2, 5]])

        self.assertEqual(n0.shape(), (2, 3))

        self.assertEqual(n0.row_layout(0), [1])
        self.assertEqual(n0.row_layout(1), [2])
        self.assertEqual(n0.row_layout(2), [3, 4])

        self.assertEqual(n0.col_layout(0), [1, 3])
        self.assertEqual(n0.col_layout(1), [2, 5])

    def test_space_size(self):
        n0 = Nonogram("black", [[1], [2], [3, 4]], [[1, 3], [2, 5]])
        self.assertEqual(n0.space_size(), 1)

        # todo
        n1 = Nonogram("color", [[1], [2], [3, 4]], [[1, 3], [2, 5]])
        self.assertEqual(n1.space_size(), 0)


if __name__ == '__main__':
    unittest.main()