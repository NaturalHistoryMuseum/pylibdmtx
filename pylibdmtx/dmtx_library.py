"""Loads libdmtx.
"""
import platform
import sys
from glob import glob

from ctypes import cdll
from ctypes.util import find_library
from pathlib import Path

__all__ = ['load']


def _windows_fname():
    """For convenience during development and to aid debugging, the DLL name is
    specific to the bit depth of interpreter.

    This logic has its own function to make testing easier
    """
    return 'libdmtx-64.dll' if sys.maxsize > 2**32 else 'libdmtx-32.dll'


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
        # First search on local folder
        _lib_search = glob(f"{Path(__file__).parent.joinpath('*dmtx*.so.*.*.*')}", recursive=True)
        path = None
        if _lib_search:
            path = _lib_search[0]
        else:
            # Assume a shared library on the path
            path = find_library('dmtx')

        if not path:
            raise ImportError('Unable to find dmtx shared library')
        libdmtx = cdll.LoadLibrary(path)

    return libdmtx
