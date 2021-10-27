import unittest

from pathlib import Path

try:
    from unittest.mock import call, patch
except ImportError:
    # Python 2
    from mock import call, patch

import numpy as np

from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import imageio
except ImportError:
    imageio = None

from pylibdmtx.pylibdmtx import (
    decode, encode, Decoded, Encoded, Rect, EXTERNAL_DEPENDENCIES
)
from pylibdmtx.pylibdmtx_error import PyLibDMTXError


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

    @classmethod
    def setUpClass(cls):
        cls.datamatrix = Image.open(str(TESTDATA.joinpath('datamatrix.png')))
        cls.empty = Image.open(str(TESTDATA.joinpath('empty.png')))

        # assertRaisesRegexp was a deprecated alias removed in Python 3.11
        if not hasattr(cls, 'assertRaisesRegex'):
            cls.assertRaisesRegex = cls.assertRaisesRegexp

    @classmethod
    def tearDownClass(cls):
        cls.datamatrix = cls.empty = None

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
        self.assertEqual([], res)

    def test_decode_numpy(self):
        "Read image using Pillow and convert to numpy.ndarray"
        res = decode(np.asarray(self.datamatrix))
        self.assertEqual(self.EXPECTED, res)

    @unittest.skipIf(imageio is None, 'imageio not installed')
    def test_decode_imageio(self):
        "Read image using imageio"
        res = decode(imageio.imread(TESTDATA.joinpath('datamatrix.png')))
        self.assertEqual(self.EXPECTED, res)

    @unittest.skipIf(cv2 is None, 'OpenCV not installed')
    def test_decode_opencv(self):
        "Read image using OpenCV"
        res = decode(cv2.imread(str(TESTDATA.joinpath('datamatrix.png'))))
        self.assertEqual(self.EXPECTED, res)

    def test_external_dependencies(self):
        "External dependencies"
        self.assertEqual(1, len(EXTERNAL_DEPENDENCIES))
        self.assertIn('libdmtx', EXTERNAL_DEPENDENCIES[0]._name)

    @patch('pylibdmtx.pylibdmtx.dmtxImageCreate')
    def test_dmtxImageCreate_failed(self, dmtxImageCreate):
        dmtxImageCreate.return_value = None
        self.assertRaisesRegex(
            PyLibDMTXError, 'Could not create image', decode, self.datamatrix
        )
        self.assertEqual(1, dmtxImageCreate.call_count)

    @patch('pylibdmtx.pylibdmtx.dmtxDecodeCreate')
    def test_dmtxDecodeCreate_failed(self, dmtxDecodeCreate):
        dmtxDecodeCreate.return_value = None
        self.assertRaisesRegex(
            PyLibDMTXError, 'Could not create decoder', decode, self.datamatrix
        )
        self.assertEqual(1, dmtxDecodeCreate.call_count)

    def test_unsupported_bits_per_pixel(self):
        # 40 bits-per-pixel
        data = (list(range(3 * 3 * 5)), 3, 3)
        self.assertRaisesRegex(
            PyLibDMTXError,
            (
                r'Unsupported bits-per-pixel: \[40\] Should be one of '
                r'\[8, 16, 24, 32\]'
            ),
            decode, data
        )

    def test_inconsistent_dimensions(self):
        # Image data has ten bytes. width x height indicates nine bytes
        data = (list(range(10)), 3, 3)
        self.assertRaisesRegex(
            PyLibDMTXError,
            (
                r'Inconsistent dimensions: image data of 10 bytes is not '
                r'divisible by \(width x height = 9\)'
            ),
            decode, data
        )


class TestEncode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # assertRaisesRegexp was a deprecated alias removed in Python 3.11
        if not hasattr(cls, 'assertRaisesRegex'):
            cls.assertRaisesRegex = cls.assertRaisesRegexp

    def _assert_encoded_data(self, expected_data, encoded):
        # Check encoded data
        image = Image.frombytes(
            'RGB', (encoded.width, encoded.height), encoded.pixels
        )
        decoded = decode(image)

        self.assertEqual(1, len(decoded))
        self.assertEqual(expected_data, decoded[0].data)

    def test_encode_defaults(self):
        data = b'hello world'
        encoded = encode(data)

        # Check returned data, with the exception of the pixel data
        self.assertEqual(
            Encoded(width=100, height=100, bpp=24, pixels=None),
            encoded._replace(pixels=None)
        )
        self._assert_encoded_data(data, encoded)

    def test_encode_size(self):
        data = b'hello world'
        encoded = encode(data, size='36x36')

        # Check returned data, with the exception of the pixel data
        self.assertEqual(
            Encoded(width=200, height=200, bpp=24, pixels=None),
            encoded._replace(pixels=None)
        )

        self._assert_encoded_data(data, encoded)

    def test_encode_scheme(self):
        data = b'hello world'
        encoded = encode(data, scheme='Base256')

        # Check returned data, with the exception of the pixel data
        self.assertEqual(
            Encoded(width=110, height=110, bpp=24, pixels=None),
            encoded._replace(pixels=None)
        )

        self._assert_encoded_data(data, encoded)

    def test_invalid_scheme(self):
        self.assertRaisesRegex(
            PyLibDMTXError,
            r"Invalid scheme \[asdf\]: should be one of \['Ascii",
            encode, b' ', scheme='asdf'
        )

    def test_invalid_size(self):
        self.assertRaisesRegex(
            PyLibDMTXError,
            r"Invalid size \[9x9\]: should be one of \['RectAuto'",
            encode, b' ', size='9x9'
        )

    def test_image_not_large_enough(self):
        self.assertRaisesRegex(
            PyLibDMTXError,
            'Could not encode data, possibly because the image is not '
            'large enough to contain the data',
            encode, b' '*50, size='10x10'
        )


if __name__ == '__main__':
    unittest.main()
