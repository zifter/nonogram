import env

import unittest

from tests.testcase_based_on_data import TestCaseBasedOnData

from base.nonogram import Nonogram
from detector.detector import Detector

class TestDetector(TestCaseBasedOnData):
    def test_detect_and_compare(self):
        test_data = self.getLayoutData()
        detector = Detector()

        for image, layout in test_data:
            n0 = Nonogram.load_from_file(layout)
            n1 = detector.recognize(image)

            self.assertEqual(n0, n1, "Detection failed: %s" % layout)

if __name__ == '__main__':
    unittest.main()