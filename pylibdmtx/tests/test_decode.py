import unittest

from pathlib import Path

import numpy as np

from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None


from pylibdmtx.pylibdmtx import decode, Decoded, Rect, EXTERNAL_DEPENDENCIES


TESTDATA = Path(__file__).parent


class TestDecode(unittest.TestCase):
    EXPECTED = [
        Decoded(
            data=b'Stegosaurus',
            rect=Rect(left=5, top=6, width=96, height=95)
        ),
        Decoded(
            data=b'Plesiosaurus',
            rect=Rect(left=298, top=6, width=95, height=95)
        )
    ]

    def setUp(self):
        self.datamatrix = Image.open(str(TESTDATA.joinpath('datamatrix.png')))
        self.empty = Image.open(str(TESTDATA.joinpath('empty.png')))

    def tearDown(self):
        self.datamatrix = self.empty = None

    def test_decode(self):
        "Read both barcodes in `datamatrix.png`"
        res = decode(self.datamatrix)
        self.assertEqual(self.EXPECTED, res)

    def test_decode_single(self):
        "Read just one of the barcodes in `datamatrix.png`"
        res = decode(self.datamatrix, max_count=1)
        self.assertEqual(self.EXPECTED[:1], res)

    def test_decode_tuple(self):
        "Read barcodes in pixels"
        pixels = self.datamatrix.copy().convert('RGB').tobytes()
        width, height = self.datamatrix.size[:2]
        res = decode((pixels, width, height))
        self.assertEqual(self.EXPECTED, res)

    def test_empty(self):
        "Do not show any output for an image that does not contain a barcode"
        res = decode(self.empty)
        expected = []
        self.assertEqual(expected, res)

    def test_decode_numpy(self):
        "Read image using Pillow and convert to numpy.ndarray"
        res = decode(np.asarray(self.datamatrix))
        self.assertEqual(self.EXPECTED, res)

    @unittest.skipIf(cv2 is None, 'OpenCV not installed')
    def test_decode_opencv(self):
        "Read image using OpenCV"
        res = decode(
            cv2.imread(str(TESTDATA.joinpath('datamatrix.png')))
        )
        self.assertEqual(self.EXPECTED, res)

    def test_external_dependencies(self):
        "External dependencies"
        self.assertEqual(1, len(EXTERNAL_DEPENDENCIES))
        self.assertIn('libdmtx', EXTERNAL_DEPENDENCIES[0]._name)


if __name__ == '__main__':
    unittest.main()
