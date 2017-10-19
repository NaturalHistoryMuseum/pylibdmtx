#!/usr/bin/env python
from __future__ import print_function

import argparse
import sys

import pylibdmtx
from pylibdmtx.pylibdmtx import encode


def parse_size(s):
    try:
        w, h = s.split('x', 1)
        w, h = int(w), int(h)
    except ValueError:
        raise argparse.ArgumentTypeError('Size is not in the format <WIDTH>x<HEIGHT>')
    return w, h


def main(args=None):
    encoding_list = 'ascii', 'base256', 'c40', 'edifact', 'text', 'x12'
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description='Creates a png file containing a datamatrix encoded message'
    )
    parser.add_argument('output_file', help='Filename of the PNG')
    parser.add_argument('message', help='Message to encode')
    parser.add_argument('--size', metavar='WxH', help='Forces datamatrix grid to WxH instead of auto size.', type=parse_size)
    parser.add_argument('--encoding-scheme', help='Forces encoding method, default is ascii', choices=encoding_list)
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
