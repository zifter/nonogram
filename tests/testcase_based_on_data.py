import env

import unittest
import os
from os.path import join

def _abs_path(rel):
    return os.path.realpath(os.path.join(os.path.dirname(__file__), rel))

class TestCaseBasedOnData(unittest.TestCase):
    def __init__(self, test_name, rel_path):
        unittest.TestCase.__init__(self, test_name)
        self.data_path = join(_abs_path("../data"), rel_path)

    def getDetectorData(self):
        result = []
        folders = os.listdir(self.data_path)

        for f in folders:
            result.append((join(self.data_path, f, "layout.png"), join(self.data_path, f, 'layout.json')))

        return result

    def getSolverData(self):
        result = []
        folders = os.listdir(self.data_path)

        for f in folders:
            result.append((join(self.data_path, f, "layout.json"), join(self.data_path, f, 'solution.json')))

        return result