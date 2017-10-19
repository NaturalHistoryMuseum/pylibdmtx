import os
import sys
import tempfile
import unittest

from pathlib import Path
from contextlib import contextmanager

if 2 == sys.version_info[0]:
    from cStringIO import StringIO
else:
    from io import StringIO


from PIL import Image

from pylibdmtx.scripts.read_datamatrix import main as main_read
from pylibdmtx.scripts.create_datamatrix import main as main_create


@contextmanager
def capture_stdout():
    sys.stdout, old_stdout = StringIO(), sys.stdout
    try:
        yield sys.stdout
    finally:
        sys.stdout = old_stdout


class TestReadDatamatrix(unittest.TestCase):
    def test_read_datamatrix(self):
        "Read datamatrix barcodes"
        with capture_stdout() as stdout:
            main_read([str(Path(__file__).parent.joinpath('datamatrix.png'))])

        if 2 == sys.version_info[0]:
            expected = "Stegosaurus\nPlesiosaurus"
        else:
            expected = "b'Stegosaurus'\nb'Plesiosaurus'"

        self.assertEqual(expected, stdout.getvalue().strip())

    def test_create_datamatrix(self):
        tmpfile = os.path.join(tempfile.mkdtemp(), 'test.png')
        main_create(['--size', '44x44', tmpfile, 'Stegosaurus'])
        with capture_stdout() as stdout:
            main_read([tmpfile])
        os.unlink(tmpfile)

        expected = "Stegosaurus" if 2 == sys.version_info[0] else "b'Stegosaurus'"
        self.assertEqual(expected, stdout.getvalue().strip())

if __name__ == '__main__':
    unittest.main()
