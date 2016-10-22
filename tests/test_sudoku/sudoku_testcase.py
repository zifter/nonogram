import env

from testcase_based_on_data import TestCaseBasedOnData

class TestNonogram(TestCaseBasedOnData):
    def __init__(self, test_name):
        TestCaseBasedOnData.__init__(self, test_name, "sudoku")