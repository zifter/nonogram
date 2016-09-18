import env

import unittest

from tests.testcase_based_on_data import TestCaseBasedOnData

from solver.layout_index import LayoutIndex

class TestLayoutIndex(TestCaseBasedOnData):
    def test_cross_out(self):
        index = LayoutIndex(4)
        index.cross_out()
        self.assertTrue(index.is_crossed_out())

    def test_unique_id(self):
        li1 = LayoutIndex(4)
        li2 = LayoutIndex(4)

        self.assertNotEqual(li1, li2)


if __name__ == '__main__':
    unittest.main()