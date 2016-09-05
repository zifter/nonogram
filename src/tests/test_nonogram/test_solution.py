import env

import unittest
import tempfile
import os

from base.solution import Solution

#--------------------------------------------------------------------------
class TestSolutionClass(unittest.TestCase):
    def test_equal_to(self):
        s0 = Solution([[1, 2], [3, 4], [5, 6]])
        s_row1 = Solution([[1, 2, 3], [3, 4], [5, 6]])
        s_row2 = Solution([[2, 1], [3, 4], [5, 6]])
        s_col1 = Solution([[1, 2], [3, 4], [5, 6], [5, 6]])
        s_col2 = Solution([[3, 4], [1, 2], [5, 6]])
        s1 = Solution([[1, 2], [3, 4], [5, 6]])

        self.assertNotEqual(s0, None)
        self.assertNotEqual(s0, s_row1, "Extra row")
        self.assertNotEqual(s0, s_row2, "Invalid value in column")
        self.assertNotEqual(s0, s_col1, "Extra column")
        self.assertNotEqual(s0, s_col2, "Invalid value in row")
        self.assertEqual(s0, s0, "The same")
        self.assertEqual(s0, s1, "The same")

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

        self.assertEqual(s0.row(0).tolist(), [1, 3, 5])
        self.assertEqual(s0.row(1).tolist(), [2, 4, 6])

        self.assertEqual(s0.col(0).tolist(), [1, 2])
        self.assertEqual(s0.col(1).tolist(), [3, 4])
        self.assertEqual(s0.col(2).tolist(), [5, 6])

        s0.row(0)[1] = 42
        self.assertEqual(s0.row(0).tolist(), [1, 42, 5])
        self.assertEqual(s0.col(1).tolist(), [42, 4])


if __name__ == '__main__':
    unittest.main()