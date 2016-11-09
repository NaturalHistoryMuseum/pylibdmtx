"""Low-level wrapper around libdmtx's interface
"""
import platform
import sys

from ctypes import (
    cdll, c_double, c_int, c_long, c_size_t, c_ubyte, c_uint, c_ulong,
    c_ulonglong, Structure, CFUNCTYPE, POINTER
)
from ctypes.util import find_library
from enum import IntEnum, unique
from pathlib import Path


# Types
c_ubyte_p = POINTER(c_ubyte)
"""unsigned char* type
"""

# Defines and enums
DmtxUndefined = -1


@unique
class DmtxProperty(IntEnum):
    DmtxPropScheme            = 100
    DmtxPropSizeRequest       = 101
    DmtxPropMarginSize        = 102
    DmtxPropModuleSize        = 103
    # Decoding properties
    DmtxPropEdgeMin           = 200
    DmtxPropEdgeMax           = 201
    DmtxPropScanGap           = 202
    DmtxPropSquareDevn        = 203
    DmtxPropSymbolSize        = 204
    DmtxPropEdgeThresh        = 205
    # Image properties
    DmtxPropWidth             = 300
    DmtxPropHeight            = 301
    DmtxPropPixelPacking      = 302
    DmtxPropBitsPerPixel      = 303
    DmtxPropBytesPerPixel     = 304
    DmtxPropRowPadBytes       = 305
    DmtxPropRowSizeBytes      = 306
    DmtxPropImageFlip         = 307
    DmtxPropChannelCount      = 308
    # Image modifiers
    DmtxPropXmin              = 400
    DmtxPropXmax              = 401
    DmtxPropYmin              = 402
    DmtxPropYmax              = 403
    DmtxPropScale             = 404


@unique
class DmtxPackOrder(IntEnum):
    DmtxPackCustom            = 100
    DmtxPack1bppK             = 200
    DmtxPack8bppK             = 300
    DmtxPack16bppRGB          = 400
    DmtxPack16bppRGBX         = 401
    DmtxPack16bppXRGB         = 402
    DmtxPack16bppBGR          = 403
    DmtxPack16bppBGRX         = 404
    DmtxPack16bppXBGR         = 405
    DmtxPack16bppYCbCr        = 406
    DmtxPack24bppRGB          = 500
    DmtxPack24bppBGR          = 501
    DmtxPack24bppYCbCr        = 502
    DmtxPack32bppRGBX         = 600
    DmtxPack32bppXRGB         = 601
    DmtxPack32bppBGRX         = 602
    DmtxPack32bppXBGR         = 603
    DmtxPack32bppCMYK         = 604


@unique
class DmtxFlip(IntEnum):
    DmtxFlipNone               = 0x00
    DmtxFlipX                  = 0x01 << 0
    DmtxFlipY                  = 0x01 << 1


# Types
DmtxPassFail = c_uint
DmtxMatrix3 = c_double * 3 * 3


# Structs
class DmtxMessage(Structure):
    _fields_ = [
        ('arraySize', c_size_t),
        ('codeSize', c_size_t),
        ('outputSize', c_size_t),
        ('outputIdx', c_int),
        ('padCount', c_int),
        ('array', c_ubyte_p),
        ('code', c_ubyte_p),
        ('output', c_ubyte_p),
    ]


class DmtxImage(Structure):
    _fields_ = [
        ('width', c_int),
        ('height', c_int),
        ('pixelPacking', c_int),
        ('bitsPerPixel', c_int),
        ('bytesPerPixel', c_int),
        ('rowPadBytes', c_int),
        ('rowSizeBytes', c_int),
        ('imageFlip', c_int),
        ('channelCount', c_int),
        ('channelStart', c_int * 4),
        ('bitsPerChannel', c_int * 4),
        ('pxl', c_ubyte_p)
    ]


class DmtxTime(Structure):
    _fields_ = [
        ('sec', c_ulonglong),      # Actually a time_t
        ('usec', c_ulong),
    ]


class DmtxPixelLoc(Structure):
    _fields_ = [
        ('X', c_int),
        ('Y', c_int),
    ]


class DmtxVector2(Structure):
    _fields_ = [
        ('X', c_double),
        ('Y', c_double),
    ]


class DmtxPointFlow(Structure):
    _fields_ = [
        ('plane', c_int),
        ('arrive', c_int),
        ('depart', c_int),
        ('mag', c_int),
        ('loc', DmtxPixelLoc),
    ]


class DmtxBestLine(Structure):
    _fields_ = [
        ('angle', c_int),
        ('hOffset', c_int),
        ('mag', c_int),
        ('stepBeg', c_int),
        ('stepPos', c_int),
        ('stepNeg', c_int),
        ('distSq', c_int),
        ('devn', c_double),
        ('locBeg', DmtxPixelLoc),
        ('locPos', DmtxPixelLoc),
        ('locNeg', DmtxPixelLoc),
    ]


class DmtxScanGrid(Structure):
    _fields_ = [
        ('minExtent', c_int),
        ('maxExtent', c_int),
        ('xOffset', c_int),
        ('yOffset', c_int),
        ('xMin', c_int),
        ('xMax', c_int),
        ('yMin', c_int),
        ('yMax', c_int),

        ('total', c_int),
        ('extent', c_int),
        ('jumpSize', c_int),
        ('pixelTotal', c_int),
        ('startPos', c_int),

        ('pixelCount', c_int),
        ('xCenter', c_int),
        ('yCenter', c_int),
    ]


class DmtxDecode(Structure):
    _fields_ = [
        ('edgeMin', c_int),
        ('edgeMax', c_int),
        ('scanGap', c_int),
        ('squareDevn', c_double),
        ('sizeIdxExpected', c_int),
        ('edgeThresh', c_int),

        ('xMin', c_int),
        ('xMax', c_int),
        ('yMin', c_int),
        ('yMax', c_int),
        ('scale', c_int),

        ('cache', c_ubyte_p),
        ('image', POINTER(DmtxImage)),
        ('grid', DmtxScanGrid),
    ]


class DmtxRegion(Structure):
    _fields_ = [
        ('jumpToPos', c_int),
        ('jumpToNeg', c_int),
        ('stepsTotal', c_int),
        ('finalPos', DmtxPixelLoc),
        ('finalNeg', DmtxPixelLoc),
        ('boundMin', DmtxPixelLoc),
        ('boundMax', DmtxPixelLoc),
        ('flowBegin', DmtxPointFlow),

        ('polarity', c_int),
        ('stepR', c_int),
        ('stepT', c_int),
        ('locR', DmtxPixelLoc),
        ('locT', DmtxPixelLoc),

        ('leftKnown', c_int),
        ('leftAngle', c_int),
        ('leftLoc', DmtxPixelLoc),
        ('leftLine', DmtxBestLine),
        ('bottomKnown', c_int),
        ('bottomAngle', c_int),
        ('bottomLoc', DmtxPixelLoc),
        ('bottomLine', DmtxBestLine),
        ('topKnown', c_int),
        ('topAngle', c_int),
        ('topLoc', DmtxPixelLoc),
        ('rightKnown', c_int),
        ('rightAngle', c_int),
        ('rightLoc', DmtxPixelLoc),

        ('onColor', c_int),
        ('offColor', c_int),
        ('sizeIdx', c_int),
        ('symbolRows', c_int),
        ('symbolCols', c_int),
        ('mappingRows', c_int),
        ('mappingCols', c_int),

        ('raw2fit', DmtxMatrix3),
        ('fit2raw', DmtxMatrix3),
    ]


# Globals populated in load_libdmtx
LIBDMTX = None
"""ctypes.CDLL
"""

EXTERNAL_DEPENDENCIES = []
"""Sequence of instances of ctypes.CDLL
"""


def load_libdmtx():
    """Loads the libdmtx shared library and its dependencies.
    """
    global LIBDMTX
    global EXTERNAL_DEPENDENCIES
    if not LIBDMTX:
        if 'Windows' == platform.system():
            # Possible scenarios here
            #   1. Run from source, DLLs are in pyzbar directory
            #       cdll.LoadLibrary() imports DLLs in repo root directory
            #   2. Wheel install into CPython installation
            #       cdll.LoadLibrary() imports DLLs in package directory
            #   3. Wheel install into virtualenv
            #       cdll.LoadLibrary() imports DLLs in package directory
            #   4. Frozen
            #       cdll.LoadLibrary() imports DLLs alongside executable

            # The DLL is specific to the bit depth of interpreter
            fname = 'libdmtx-64.dll' if sys.maxsize > 2**32 else 'libdmtx-32.dll'
            try:
                libdmtx = cdll.LoadLibrary(fname)
            except OSError as e:
                libdmtx = cdll.LoadLibrary(
                    str(Path(__file__).parent.joinpath(fname))
                )
        else:
            # Assume a shared library on the path
            path = find_library('dmtx')
            if not path:
                raise ImportError('Unable to find dmtx shared library')
            libdmtx = cdll.LoadLibrary(path)

        LIBDMTX = libdmtx
        EXTERNAL_DEPENDENCIES = [LIBDMTX]

    return LIBDMTX


# Function signatures
def libdmtx_function(fname, restype, *args):
    """Returns a foreign function exported by `libdmtx`.

    Args:
        fname (:obj:`str`): Name of the exported function as string.
        restype (:obj:): Return type - one of the `ctypes` primitive C data
        types.
        *args: Arguments - a sequence of `ctypes` primitive C data types.

    Returns:
        cddl.CFunctionType: A wrapper around the function.
    """
    prototype = CFUNCTYPE(restype, *args)
    return prototype((fname, load_libdmtx()))


dmtxTimeNow = libdmtx_function('dmtxTimeNow', DmtxTime)

dmtxTimeAdd = libdmtx_function(
    'dmtxTimeAdd',
    DmtxTime,
    DmtxTime,    # t
    c_long       # msec
)

dmtxDecodeCreate = libdmtx_function(
    'dmtxDecodeCreate',
    POINTER(DmtxDecode),
    POINTER(DmtxImage),    # img
    c_int,      # scale
)

dmtxDecodeDestroy = libdmtx_function(
    'dmtxDecodeDestroy',
    DmtxPassFail,
    POINTER(POINTER(DmtxDecode))
)


dmtxDecodeSetProp = libdmtx_function(
    'dmtxDecodeSetProp',
    DmtxPassFail,
    POINTER(DmtxDecode),
    c_int,    # prop
    c_int     # value
)

dmtxImageCreate = libdmtx_function(
    'dmtxImageCreate',
    POINTER(DmtxImage),
    POINTER(c_ubyte),    # pxl
    c_int,     # width
    c_int,     # height
    c_int      # pack
)

dmtxImageDestroy = libdmtx_function(
    'dmtxImageDestroy',
    DmtxPassFail,
    POINTER(POINTER(DmtxImage))
)

dmtxRegionFindNext = libdmtx_function(
    'dmtxRegionFindNext',
    POINTER(DmtxRegion),
    POINTER(DmtxDecode),
    POINTER(DmtxTime)    # timeout
)

dmtxDecodeMatrixRegion = libdmtx_function(
    'dmtxDecodeMatrixRegion',
    POINTER(DmtxMessage),
    POINTER(DmtxDecode),    # dec
    POINTER(DmtxRegion),    # reg
    c_int,                  # fix
)

dmtxMatrix3VMultiplyBy = libdmtx_function(
    'dmtxMatrix3VMultiplyBy',
    c_int,
    POINTER(DmtxVector2),
    DmtxMatrix3,
)

dmtxMessageDestroy = libdmtx_function(
    'dmtxMessageDestroy',
    DmtxPassFail,
    POINTER(POINTER(DmtxMessage))
)

dmtxRegionDestroy = libdmtx_function(
    'dmtxRegionDestroy',
    DmtxPassFail,
    POINTER(POINTER(DmtxRegion))
)
