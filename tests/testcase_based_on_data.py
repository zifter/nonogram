import env

import unittest
import os
import re
from os.path import join

def _abs_path(rel):
    return os.path.realpath(os.path.join(os.path.dirname(__file__), rel))

class TestCaseBasedOnData(unittest.TestCase):
    def __init__(self, test_name, rel_path):
        unittest.TestCase.__init__(self, test_name)
        self.data_path = join(_abs_path("../data"), rel_path)

    def getLayoutData(self):
        result = []
        files = os.listdir(self.data_path)

        pattern = re.compile(r"([0-9]+)_layout.json")
        for f in files:
            matchResult = pattern.match(f)
            if matchResult:
                name = matchResult.group(1)
                result.append((join(self.data_path, "%s_layout.png" % name), join(self.data_path, f)))

        return result

    def getSolutionData(self):
        result = []
        files = os.listdir(self.data_path)

        pattern = re.compile(r"([0-9]+)_sol.json")
        for f in files:
            matchResult = pattern.match(f)
            if matchResult:
                name = matchResult.group(1)
                result.append((join(self.data_path, "%s_layout.json" % name), join(self.data_path, f)))

        return result