# pylibdmtx

[![Travis status](https://travis-ci.org/NaturalHistoryMuseum/pylibdmtx.svg?branch=master)](https://travis-ci.org/NaturalHistoryMuseum/pylibdmtx)
[![Python Versions](https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5-blue.svg)](https://github.com/NaturalHistoryMuseum/pylibdmtx)
[![Coverage Status](https://coveralls.io/repos/github/NaturalHistoryMuseum/pylibdmtx/badge.svg?branch=master)](https://coveralls.io/github/NaturalHistoryMuseum/pylibdmtx?branch=master)

A `ctypes`-based Python wrapper around the [libdmtx](http://libdmtx.sourceforge.net/)
datamatrix barcode reader.

The [pydmtx](https://sourceforge.net/p/libdmtx/dmtx-wrappers/ci/master/tree/python/)
wrapper is stuck in Python 2.x-land. This `ctypes`-based wrapper brings
`libdmtx` to 2.7 and to 3.4 or greater.

## Installation

Install the `libdmtx` shared lib. On Mac OS X:

```
brew install libdmtx
```

On Linux:

```
sudo apt-get install libdmtx0a
```

Install this Python wrapper:

```
pip install pylibdmtx
```

The `libdmtx` `DLL`s are included with the Windows Python wheel.

## Example usage

The `decode` function accepts instances of `PIL.Image`

```
>>> from pylibdmtx.pylibdmtx import decode
>>> from PIL import Image
>>> decode(Image.open('pylibdmtx/tests/datamatrix.png'))
[Decoded(data='Stegosaurus', rect=Rect(left=5, top=6, width=96, height=95)),
 Decoded(data='Plesiosaurus', rect=Rect(left=298, top=6, width=95, height=95))]
```

It also accepts instances of `numpy.ndarray`, which might come from loading
images using OpenCV

```
>>> import cv2
>>> decode(cv2.imread('pylibdmtx/tests/datamatrix.png'))
[Decoded(data='Stegosaurus', rect=Rect(left=5, top=6, width=96, height=95)),
 Decoded(data='Plesiosaurus', rect=Rect(left=298, top=6, width=95, height=95))]
```

You can also provide a tuple `(pixels, width, height)`

```
>>> image = cv2.imread('pylibdmtx/tests/datamatrix.png')
>>> height, width = image.shape[:2]
>>> decode((image.tobytes(), width, height))
[Decoded(data='Stegosaurus', rect=Rect(left=5, top=6, width=96, height=95)),
 Decoded(data='Plesiosaurus', rect=Rect(left=298, top=6, width=95, height=95))]
```

## Limitations

Feel free to submit a PR to address any of these.

* Decoding only - no encoding

* I took the bone-headed approach of copying the logic in
`pydmtx`'s `decode` function
(in [`pydmtxmodule.c`](https://sourceforge.net/p/libdmtx/dmtx-wrappers/ci/master/tree/python/))
- there might be more of `libdmtx`'s functionality that could be used to read
barcodes

* I exposed the bare minimum of functions, defines, enums and typedefs
neede to reimplement `pydmtx`'s `decode` function

## License

`pylibdmtx` is distributed under the MIT license (see `LICENCE.txt`).
The `libdmtx` shared library is distributed under the Simplified BSD license
(see `pylibdmtx/lib/libdmtx-LICENCE.txt`)
