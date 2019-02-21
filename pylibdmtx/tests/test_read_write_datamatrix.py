import os
import sys
import tempfile
import unittest

from pathlib import Path
from contextlib import contextmanager

# TODO Would io.StringIO not work in all cases?
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from pylibdmtx.scripts.read_datamatrix import main as main_read
from pylibdmtx.scripts.write_datamatrix import main as main_write


@contextmanager
def capture_stdout():
    sys.stdout, old_stdout = StringIO(), sys.stdout
    try:
        yield sys.stdout
    finally:
        sys.stdout = old_stdout


class TestReadWriteDatamatrix(unittest.TestCase):
    def test_read_datamatrix(self):
        "Read datamatrix barcodes"
        with capture_stdout() as stdout:
            main_read([str(Path(__file__).parent.joinpath('datamatrix.png'))])

        if 2 == sys.version_info[0]:
            expected = "Stegosaurus\nPlesiosaurus"
        else:
            expected = "b'Stegosaurus'\nb'Plesiosaurus'"

        self.assertEqual(expected, stdout.getvalue().strip())

    def test_write_datamatrix(self):
        tmpfile = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        tmpfile.close()
        try:
            main_write(['--size', '44x44', tmpfile.name, 'Stegosaurus'])
            with capture_stdout() as stdout:
                main_read([tmpfile.name])

            expected = (
                "Stegosaurus" if 2 == sys.version_info[0] else "b'Stegosaurus'"
            )
            self.assertEqual(expected, stdout.getvalue().strip())
        finally:
            os.unlink(tmpfile.name)


if __name__ == '__main__':
    unittest.main()
