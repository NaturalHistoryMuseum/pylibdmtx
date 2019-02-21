import unittest

from pathlib import Path

try:
    from unittest.mock import call, patch
except ImportError:
    # Python 2
    from mock import call, patch

from pylibdmtx import dmtx_library


class TestLoad(unittest.TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)
        self.cdll = patch(
            'pylibdmtx.dmtx_library.cdll', autospec=True
        ).start()
        self.find_library = patch(
            'pylibdmtx.dmtx_library.find_library', autospec=True
        ).start()
        self.platform = patch(
            'pylibdmtx.dmtx_library.platform', autospec=True
        ).start()
        self.windows_fname = patch(
            'pylibdmtx.dmtx_library._windows_fname', autospec=True,
            return_value='dll fname'
        ).start()

    def test_found_non_windows(self):
        "libdmtx loaded ok on non-Windows platform"
        self.platform.system.return_value = 'Not windows'

        res = dmtx_library.load()

        self.platform.system.assert_called_once_with()
        self.find_library.assert_called_once_with('dmtx')
        self.cdll.LoadLibrary.assert_called_once_with(
            self.find_library.return_value
        )

        self.assertEqual(self.cdll.LoadLibrary.return_value, res)
        self.assertEqual(0, self.windows_fname.call_count)

    def test_not_found_non_windows(self):
        "libdmtx not found on non-Windows platform"
        self.platform.system.return_value = 'Not windows'
        self.find_library.return_value = None

        self.assertRaises(ImportError, dmtx_library.load)

        self.platform.system.assert_called_once_with()
        self.find_library.assert_called_once_with('dmtx')

    def test_found_windows(self):
        "libdmtx found on Windows"
        self.platform.system.return_value = 'Windows'

        res = dmtx_library.load()

        self.platform.system.assert_called_once_with()
        self.cdll.LoadLibrary.assert_called_once_with(
            self.windows_fname.return_value
        )
        self.assertEqual(self.cdll.LoadLibrary.return_value, res)

    def test_found_second_attempt_windows(self):
        "libdmtx found on the second attempt on Windows"
        self.platform.system.return_value = 'Windows'
        self.cdll.LoadLibrary.side_effect = [
            OSError,            # First call does not load DLL
            'loaded library',   # Second call loads DLL
        ]

        res = dmtx_library.load()

        self.platform.system.assert_called_once_with()
        self.cdll.LoadLibrary.assert_has_calls([
            call(self.windows_fname.return_value),
            call(str(Path(dmtx_library.__file__).parent.joinpath(
                self.windows_fname.return_value
            ))),
        ])

        self.assertEqual('loaded library', res)

    def test_not_found_windows(self):
        "libdmtx not found on Windows"
        self.platform.system.return_value = 'Windows'
        self.cdll.LoadLibrary.side_effect = OSError

        self.assertRaises(OSError, dmtx_library.load)

        self.platform.system.assert_called_once_with()
        # Two attempts at loading
        self.cdll.LoadLibrary.assert_has_calls([
            call(self.windows_fname.return_value),
            call(str(Path(dmtx_library.__file__).parent.joinpath(
                self.windows_fname.return_value
            ))),
        ])


class TestWindowsFname(unittest.TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)
        self.sys = patch('pylibdmtx.dmtx_library.sys', autospec=True).start()

    def test_32bit(self):
        self.sys.maxsize = 2**32
        self.assertEqual('libdmtx-32.dll', dmtx_library._windows_fname())

    def test_64bit(self):
        # This is a 'long' on a 32-bit interpreter
        self.sys.maxsize = 2**32 + 1
        self.assertEqual('libdmtx-64.dll', dmtx_library._windows_fname())


if __name__ == '__main__':
    unittest.main()
