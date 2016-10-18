import env

import unittest

from tests.testcase_based_on_data import TestCaseBasedOnData

from solver.layout_index import *

class TestLayoutIndex(TestCaseBasedOnData):
    def test_cross_out(self):
        index = LayoutIndex(4)
        index.cross_out()
        self.assertTrue(index.is_crossed_out())

    def test_unique_id(self):
        li1 = LayoutIndex(4)
        li2 = LayoutIndex(4)

        self.assertNotEqual(li1, li2)

class TestSmartTuple(TestCaseBasedOnData):
    def test_smart_tuple_equlity(self):
        sm1 = SmartTuple(1, 2)
        sm2 = SmartTuple(2, 3)
        sm3 = SmartTuple(2, 1)

        self.assertTrue(sm1.test_eq1(1))
        self.assertTrue(sm1.test_eq1(2))

        self.assertTrue(sm1.tuple_eq1(sm1))
        self.assertTrue(sm1.tuple_eq1(sm2))
        self.assertTrue(sm1.tuple_eq1(sm3))

        self.assertTrue(sm1.tuple_eq2(sm1))
        self.assertFalse(sm1.tuple_eq2(sm2))
        self.assertTrue(sm1.tuple_eq2(sm3))

    def test_smart_tuple_equlity_soft(self):
        sm1 = SoftTuple(1, 2)
        sm2 = SoftTuple(2, 3)

        self.assertEqual(sm1, sm2)
        self.assertEqual(sm1, (None, 1))
        self.assertEqual(sm1, (None, 1))
        self.assertEqual(sm1, (2, None))
        self.assertNotEqual(sm1, (3, 4))


    def test_smart_tuple_equlity_strict(self):
        sm1 = StrictTuple(1, 2)
        sm2 = StrictTuple(2, 3)

        self.assertNotEqual(sm1, sm2)
        self.assertNotEqual(sm1, (None, 1))
        self.assertNotEqual(sm1, (None, 1))
        self.assertNotEqual(sm1, (2, None))
        self.assertNotEqual(sm1, (2, 1))

    def test_smart_tuple_equal(self):
        sm1 = SmartTuple(1, 2)
        sm1[0] = 3

        self.assertEqual(sm1[0], 3)

if __name__ == '__main__':
    unittest.main()