import sys
import unittest

from pathlib import Path
from contextlib import contextmanager

if 2 == sys.version_info[0]:
    from cStringIO import StringIO
else:
    from io import StringIO


from PIL import Image

from pylibdmtx.scripts.read_datamatrix import main


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
            main([str(Path(__file__).parent.joinpath('datamatrix.png'))])

        if 2 == sys.version_info[0]:
            expected = "Stegosaurus\nPlesiosaurus"
        else:
            expected = "b'Stegosaurus'\nb'Plesiosaurus'"

        self.assertEqual(expected, stdout.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
