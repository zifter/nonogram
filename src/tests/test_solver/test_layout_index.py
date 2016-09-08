import env

import unittest

from tests.testcase_based_on_data import TestCaseBasedOnData

from solver.layout_index import LayoutIndex

class TestLayoutIndex(TestCaseBasedOnData):
    def test_cross_out(self):
        index = LayoutIndex(4, 42)

        index.cross_out()

        self.assertTrue(index.is_crossed_out())
        self.assertEqual(index.id(), 42)

if __name__ == '__main__':
    unittest.main()