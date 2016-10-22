import env

import unittest
import tempfile
import os

from test_nonogram.nonogram_testcase import TestNonogram
from nonogram.solution import Solution

#--------------------------------------------------------------------------
class TestSolutionClass(TestNonogram):
    def test_load(self):
        s0 = Solution([[1, 2], [3, 4], [5, 6]])
        s1 = Solution.load({"matrix": [[1, 2], [3, 4], [5, 6]]})

        self.assertEqual(s0, s1)

    def test_save(self):
        s0 = Solution([[1, 2], [3, 4], [5, 6]])

        self.assertEqual(s0.save(), {"matrix": [[1, 2], [3, 4], [5, 6]]})

    def test_save_and_load_using_file(self):
        handler, tmpfile = tempfile.mkstemp(prefix="solution_")

        try:
            s0 = Solution([[1, 2], [3, 4], [5, 6]])
            s0.save_to_file(tmpfile)

            s1 = Solution.load_from_file(tmpfile)

            self.assertEqual(s0, s1)
        finally:
            os.close(handler)
            os.remove(tmpfile)

    def test_col_and_row_getter_with_modifier(self):
        s0 = Solution([[1, 2], [3, 4], [5, 6]])

        self.assertEqual(s0.col(0), [1, 3, 5])
        self.assertEqual(s0.col(1), [2, 4, 6])

        self.assertEqual(s0.row(0), [1, 2])
        self.assertEqual(s0.row(1), [3, 4])
        self.assertEqual(s0.row(2), [5, 6])

        s0.item(1, 0).v = 42
        self.assertEqual(s0.col(0), [1, 42, 5])
        self.assertEqual(s0.row(1), [42, 4])


if __name__ == '__main__':
    unittest.main()