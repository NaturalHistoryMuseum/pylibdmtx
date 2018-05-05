import unittest
from PIL import Image

from pylibdmtx.pylibdmtx import encode, decode
from pylibdmtx.pylibdmtx_error import PyLibDMTXError


class TestEncode(unittest.TestCase):
    def test_encode(self):
        data = b'hello_world'
        w, h, bpp, pxl = encode(data)
        self.assertEqual(bpp, 24)
        im = Image.frombytes('RGB', (w, h), pxl)
        dec_data = decode(im)
        self.assertEqual(dec_data[0] .data, data)

        w2, h2, bpp, pxl = encode(data, symsize='36x36', scheme='text')
        im = Image.frombytes('RGB', (w2, h2), pxl)
        dec_data = decode(im)
        self.assertEqual(dec_data[0].data, data)
        self.assertGreater(w2, w)
        self.assertGreater(h2, h)

    def test_errors(self):
        self.assertRaises(ValueError, encode, b' ', scheme='asdf')
        self.assertRaises(ValueError, encode, b' ', symsize=(2,2))
        self.assertRaises(PyLibDMTXError, encode, b' '*50, symsize='10x10')


if __name__ == '__main__':
    unittest.main()
