"""Loads libdmtx.
"""
import platform
import sys
import os
import re

from ctypes import cdll
from ctypes.util import find_library
from pathlib import Path

__all__ = ['load']
_lib_name = 'dmtx'


def _windows_fname():
    """For convenience during development and to aid debugging, the DLL name is
    specific to the bit depth of interpreter.

    This logic has its own function to make testing easier
    """
    return f'lib{_lib_name}-64.dll' if sys.maxsize > 2**32 else f'lib{_lib_name}-32.dll'


def load():
    """Loads the libdmtx shared library.
    """
    if 'Windows' == platform.system():
        # Possible scenarios here
        #   1. Run from source, DLLs are in pylibdmtx directory
        #       cdll.LoadLibrary() imports DLLs in repo root directory
        #   2. Wheel install into CPython installation
        #       cdll.LoadLibrary() imports DLLs in package directory
        #   3. Wheel install into virtualenv
        #       cdll.LoadLibrary() imports DLLs in package directory
        #   4. Frozen
        #       cdll.LoadLibrary() imports DLLs alongside executable

        fname = _windows_fname()
        try:
            libdmtx = cdll.LoadLibrary(fname)
        except OSError:
            libdmtx = cdll.LoadLibrary(
                str(Path(__file__).parent.joinpath(fname))
            )
    else:
        # Assume a shared library on the path
        path = find_library(_lib_name)
        if not path:
            # Search on local folder
            _base_path = Path(__file__).parent.absolute()
            # linux do put 'lib' as name prefix and can put the version after the extension (e.g. libdmtx.so.0.1.0 )
            _lib_search = [f for f in os.listdir(_base_path) if re.search(rf'[a-z]*{_lib_name}[a_z]*.so[.0-9]*', f)]
            if _lib_search:
                path = _base_path.joinpath(_lib_search[0])

        if not path:
            raise ImportError('Unable to find dmtx shared library')
        libdmtx = cdll.LoadLibrary(path)

    return libdmtx
