#!/usr/bin/env python
from __future__ import print_function

import argparse
import sys

import pylibdmtx
from pylibdmtx.pylibdmtx import (
    encode, ENCODING_SIZE_NAMES, ENCODING_SCHEME_NAMES
)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description='Writes a datamatrix barcode to a new image file'
    )
    parser.add_argument('file', help='Filename of the output image')
    parser.add_argument(
        'data', help='Data to be written; will be utf-8 encoded'
    )
    parser.add_argument(
        '--size',
        help="Encoding size (not image dimensions); default is 'ShapeAuto'",
        choices=ENCODING_SIZE_NAMES
    )
    parser.add_argument(
        '--scheme',
        help="Encoding method; default is 'Ascii'",
        choices=ENCODING_SCHEME_NAMES
    )
    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s ' + pylibdmtx.__version__
    )
    args = parser.parse_args(args)

    from PIL import Image

    encoded = encode(
        args.data.encode('utf-8'), size=args.size, scheme=args.scheme
    )
    im = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    im.save(args.file)


if __name__ == '__main__':
    main()
