import os
import sys
import tempfile
import unittest

from PIL import Image
from PIL import ImageChops
from pathlib import Path
from contextlib import contextmanager

# TODO Would io.StringIO not work in all cases?
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from pylibdmtx.scripts.read_datamatrix import main as main_read
from pylibdmtx.scripts.write_datamatrix import main as main_write
from pylibdmtx.wrapper import dmtxVersion, dmtxHasReaderProgramming


@contextmanager
def capture_stdout():
    sys.stdout, old_stdout = StringIO(), sys.stdout
    try:
        yield sys.stdout
    finally:
        sys.stdout = old_stdout


class TestReaderProgramming(unittest.TestCase):

    def test_libdmtx_version(self):
        """Check feature availability on minimum version and if it was compiled."""
        self.assertGreaterEqual(dmtxVersion(), '1.0.0', 'Feature not present on older library version.')
        self.assertEqual(dmtxHasReaderProgramming(), True, 'Feature not built on loaded library.')

    def test_read_datamatrix_reader_programming(self):
        """Read datamatrix reader programming barcodes."""
        with capture_stdout() as stdout:
            main_read([str(Path(__file__).parent.joinpath('reader_programming.bmp'))])

        if 2 == sys.version_info[0]:
            expected = "$P\\r"
        else:
            expected = "b'$P\\r'"

        self.assertEqual(expected, stdout.getvalue().strip())

    def test_write_reader_programming_datamatrix(self):
        """Create reader programming datamatrix and read it."""
        tmpfile = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        tmpfile.close()
        try:
            main_write(['--reader-programming', '--size', '16x16', tmpfile.name, '$P\r'])
            with capture_stdout() as stdout:
                main_read([tmpfile.name])

            expected = (
                "$P\\r" if 2 == sys.version_info[0] else "b'$P\\r'"
            )
            self.assertEqual(expected, stdout.getvalue().strip())
        finally:
            os.unlink(tmpfile.name)

    def test_compare_reader_programming_images(self):
        """Compare output image with existing correct one."""
        tmpfile = tempfile.NamedTemporaryFile(suffix='.bmp', delete=False)
        tmpfile.close()
        try:
            main_write(['--reader-programming', '--size', '16x16', tmpfile.name, '$P\r'])

            _expected_image = Image.open(Path(__file__).parent.joinpath('reader_programming.bmp'))
            _created_image = Image.open(tmpfile.name)

            diff = ImageChops.difference(_expected_image, _created_image)

            self.assertEqual(diff.getbbox(), None)
        finally:
            os.unlink(tmpfile.name)


if __name__ == '__main__':
    unittest.main()
