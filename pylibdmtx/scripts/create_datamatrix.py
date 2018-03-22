#!/usr/bin/env python
from __future__ import print_function

import argparse
import sys

import pylibdmtx
from pylibdmtx.pylibdmtx import encode, ENCODING_SIZE_NAMES, ENCODING_SCHEME_NAMES


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description='Creates an image containing a datamatrix encoded message'
    )
    parser.add_argument('output_file', help='Filename of the output image')
    parser.add_argument('message', help='Message to encode')
    parser.add_argument('--size', metavar='WxH', help='Forces datamatrix grid to WxH instead of auto size.', choices=ENCODING_SIZE_NAMES)
    parser.add_argument('--encoding-scheme', help='Forces encoding method, default is ascii', choices=ENCODING_SCHEME_NAMES)
    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s ' + pylibdmtx.__version__
    )
    args = parser.parse_args(args)

    from PIL import Image

    w, h, bpp, pixels = encode(args.message.encode(), symsize=args.size, scheme=args.encoding_scheme)
    im = Image.frombytes('RGB', (w, h),pixels)
    im.save(args.output_file)

if __name__ == '__main__':
    main()
