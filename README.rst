pylibdmtx
=========

.. image:: https://img.shields.io/badge/python-3.10%2C%203.11%2C%203.12%2C%203.13-blue.svg
    :target: https://github.com/NaturalHistoryMuseum/pylibdmtx

.. image:: https://badge.fury.io/py/pylibdmtx.svg
    :target: https://pypi.python.org/pypi/pylibdmtx

.. image:: https://img.shields.io/github/actions/workflow/status/NaturalHistoryMuseum/pylibdmtx/test.yml?label=tests
    :target: https://github.com/NaturalHistoryMuseum/pylibdmtx/actions/workflows/test.yml

.. image:: https://coveralls.io/repos/github/NaturalHistoryMuseum/pylibdmtx/badge.svg?branch=master
    :target: https://coveralls.io/github/NaturalHistoryMuseum/pylibdmtx?branch=master

Read and write Data Matrix barcodes from Python 3 using the
`libdmtx <http://libdmtx.sourceforge.net/>`__ library.

-  Pure python
-  Works with PIL / Pillow images, OpenCV / imageio / numpy ``ndarray``\ s, and raw bytes
-  Decodes locations of barcodes
-  No dependencies, other than the libdmtx library itself
-  Tested on Python 3.10 to 3.13

The older
`pydmtx <https://sourceforge.net/p/libdmtx/dmtx-wrappers/ci/master/tree/python/>`__
package is stuck in Python 2.x-land.

Installation
------------

The ``libdmtx`` ``DLL``\ s are included with the Windows Python wheels.
On other operating systems, you will need to install the ``libdmtx`` shared
library.

Mac OS X:

::

   brew install libdmtx

Linux:

::

   sudo apt-get install libdmtx0t64

The PyPI package is currently out-of-date; to install the latest version, use:

::

    pip install git+https://github.com/NaturalHistoryMuseum/pylibdmtx.git

To use the
``read_datamatrix`` and ``write_datamatrix`` command-line scripts, you will also need to install Pillow >= 3.2.0:

::

    pip install "Pillow>=3.2.0"

If you want to install the outdated package from PyPI:

::

   pip install pylibdmtx
   pip install pylibdmtx[scripts]

Example usage
-------------

The ``decode`` function accepts instances of ``PIL.Image``.

::

   >>> from pylibdmtx.pylibdmtx import decode
   >>> from PIL import Image
   >>> decode(Image.open('pylibdmtx/tests/datamatrix.png'))
   [Decoded(data='Stegosaurus', rect=Rect(left=5, top=6, width=96, height=95)),
    Decoded(data='Plesiosaurus', rect=Rect(left=298, top=6, width=95, height=95))]

It also accepts instances of ``numpy.ndarray``, which might come from loading
images using `OpenCV <http://opencv.org/>`__.

::

   >>> import cv2
   >>> decode(cv2.imread('pylibdmtx/tests/datamatrix.png'))
   [Decoded(data='Stegosaurus', rect=Rect(left=5, top=6, width=96, height=95)),
    Decoded(data='Plesiosaurus', rect=Rect(left=298, top=6, width=95, height=95))]

You can also provide a tuple ``(pixels, width, height)``

::

   >>> image = cv2.imread('pylibdmtx/tests/datamatrix.png')
   >>> height, width = image.shape[:2]
   >>> decode((image.tobytes(), width, height))
   [Decoded(data='Stegosaurus', rect=Rect(left=5, top=6, width=96, height=95)),
    Decoded(data='Plesiosaurus', rect=Rect(left=298, top=6, width=95, height=95))]

The ``encode`` function generates an image containing a Data Matrix barcode:

::

  >>> from pylibdmtx.pylibdmtx import encode
  >>> encoded = encode('hello world'.encode('utf8'))
  >>> img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
  >>> img.save('dmtx.png')
  >>> print(decode(Image.open('dmtx.png')))
  [Decoded(data=b'hello world', rect=Rect(left=9, top=10, width=80, height=79))]

Windows error message
---------------------

If you see an ugly ``ImportError`` when importing ``pylibdmtx`` on
Windows you will most likely need the `Visual C++ Redistributable Packages for
Visual Studio 2013
<https://www.microsoft.com/en-US/download/details.aspx?id=40784>`__.
Install ``vcredist_x64.exe`` if using 64-bit Python, ``vcredist_x86.exe`` if
using 32-bit Python.

Limitations
-----------

Feel free to submit a PR to address any of these.

-  I took the bone-headed approach of copying the logic in
   ``pydmtx``\ ’s ``decode`` function (in
   `pydmtxmodule.c <https://sourceforge.net/p/libdmtx/dmtx-wrappers/ci/master/tree/python/>`__); there might be more of ``libdmtx``\ ’s functionality that could usefully
   be exposed

-  I exposed the bare minimum of functions, defines, enums and typedefs neede to
   reimplement ``pydmtx``\ ’s ``decode`` function

Contributors
------------

-  Vinicius Kursancew (@kursancew) - first implementation of barcode writing
-  Joseph Weston (@jbweston) - support for ``libdmtx`` 0.7.5

License
-------

``pylibdmtx`` is distributed under the MIT license (see ``LICENCE.txt``).
The ``libdmtx`` shared library is distributed under the Simplified BSD license
(see ``libdmtx-LICENCE.txt``).
