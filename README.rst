pylibdmtx
=========

.. image:: https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg
    :target: https://github.com/NaturalHistoryMuseum/pylibdmtx

.. image:: https://badge.fury.io/py/pylibdmtx.svg
    :target: https://pypi.python.org/pypi/pylibdmtx

.. image:: https://travis-ci.org/NaturalHistoryMuseum/pylibdmtx.svg?branch=master
    :target: https://travis-ci.org/NaturalHistoryMuseum/pylibdmtx

.. image:: https://coveralls.io/repos/github/NaturalHistoryMuseum/pylibdmtx/badge.svg?branch=master
    :target: https://coveralls.io/github/NaturalHistoryMuseum/pylibdmtx?branch=master

Read and write Data Matrix barcodes from Python 2 and 3 using the
`libdmtx <http://libdmtx.sourceforge.net/>`__ library.

-  Pure python
-  Works with PIL / Pillow images, OpenCV / numpy ``ndarray``\ s, and raw bytes
-  Decodes locations of barcodes
-  No dependencies, other than the libdmtx library itself
-  Tested on Python 2.7, and Python 3.4 to 3.6

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

   sudo apt-get install libdmtx0a

Install this Python wrapper; use the second form to install dependencies of the
``read_datamatrix`` and ``write_datamatrix`` command-line scripts:

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
  >>> encoded = encode('hello world')
  >>> img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
  >>> img.save('dmtx.png')


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

License
-------

``pylibdmtx`` is distributed under the MIT license (see ``LICENCE.txt``).
The ``libdmtx`` shared library is distributed under the Simplified BSD license
(see ``libdmtx-LICENCE.txt``).
