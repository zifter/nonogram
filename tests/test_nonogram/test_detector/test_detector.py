import env

import unittest

from test_nonogram.testcase_nonogram import TestCaseNonogram

from nonogram.nonogram_obj import Nonogram
from nonogram.detector.detector import Detector

class TestDetector(TestCaseNonogram):
    def test_detect_and_compare(self):
        test_data = self.getLayoutData()
        detector = Detector()

        for image, layout in test_data:
            n0 = Nonogram.load_from_file(layout)
            n1 = detector.recognize(image)

            self.assertEqual(n0, n1, "Detection failed: %s" % layout)

if __name__ == '__main__':
    unittest.main()