import env

import unittest
import tempfile
import os

from test_sudoku.testcase_sudoku import TestCaseSudoku
from sudoku.solution import Solution


class TestSudokuSolutionClass(TestCaseSudoku):
    matrix = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],  # 1
        [1, 2, 3, 4, 5, 6, 7, 8, 9],  # 2
        [1, 2, 3, 4, 5, 6, 7, 8, 9],  # 3
        [1, 2, 3, 4, 5, 6, 7, 8, 9],  # 4
        [1, 2, 3, 4, 5, 6, 7, 8, 9],  # 5
        [1, 2, 3, 4, 5, 6, 7, 8, 9],  # 6
        [1, 2, 3, 4, 5, 6, 7, 8, 9],  # 7
        [1, 2, 3, 4, 5, 6, 7, 8, 9],  # 8
        [1, 2, 3, 4, 5, 6, 7, 8, 9],  # 9
    ]

    def test_load(self):
        s0 = Solution(self.matrix)
        s1 = Solution.load({"matrix": self.matrix})

        self.assertEqual(s0, s1)

    def test_save(self):
        s0 = Solution(self.matrix)

        self.assertEqual(s0.save(), {"matrix": self.matrix})

    def test_save_and_load_using_file(self):
        handler, tmpfile = tempfile.mkstemp(prefix="solution_")

        try:
            s0 = Solution(matrix=self.matrix)
            s0.save_to_file(tmpfile)

            s1 = Solution.load_from_file(tmpfile)

            self.assertEqual(s0, s1)
        finally:
            os.close(handler)
            os.remove(tmpfile)


if __name__ == '__main__':
    unittest.main()