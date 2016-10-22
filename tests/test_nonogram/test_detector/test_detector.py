import env

import unittest

from test_nonogram.nonogram_testcase import TestNonogram

from nonogram.base.nonogram_obj import Nonogram
from nonogram.detector.detector import Detector

class TestDetector(TestNonogram):
    def test_detect_and_compare(self):
        test_data = self.getLayoutData()
        detector = Detector()

        for image, layout in test_data:
            n0 = Nonogram.load_from_file(layout)
            n1 = detector.recognize(image)

            self.assertEqual(n0, n1, "Detection failed: %s" % layout)

if __name__ == '__main__':
    unittest.main()