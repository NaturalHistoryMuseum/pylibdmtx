from collections import namedtuple
from contextlib import contextmanager
from ctypes import cast, string_at

from .pylibdmtx_error import PyLibDMTXError
from .wrapper import (
   c_ubyte_p, dmtxImageCreate, dmtxImageDestroy, dmtxDecodeCreate,
   dmtxDecodeDestroy, dmtxRegionDestroy, dmtxMessageDestroy, dmtxTimeAdd,
   dmtxTimeNow, dmtxDecodeMatrixRegion, dmtxRegionFindNext,
   dmtxMatrix3VMultiplyBy,
   DmtxFlip, DmtxPackOrder, DmtxProperty, DmtxUndefined, DmtxVector2
)


# A rectangle
Rect = namedtuple('Rect', ['left', 'top', 'width', 'height'])

# Results of reading a barcode
Decoded = namedtuple('Decoded', ['data', 'rect'])


@contextmanager
def libdmtx_image(pixels, width, height, pack):
   """A context manager for `DmtxImage`, created and destoyed by
   `dmtxImageCreate` and `dmtxImageDestroy`.

   Args:
      pixels (:obj:):
      width (int):
      height (int):
      pack (int):

   Yields:
      DmtxImage: The created image

   Raises:
      PyLibDMTXError: If the image could not be created.
   """
   image = dmtxImageCreate(pixels, width, height, pack)
   if not image:
      raise PyLibDMTXError('Could not create image')
   else:
      try:
         yield image
      finally:
         dmtxImageDestroy(image)


@contextmanager
def libdmtx_decoder(image, shrink):
   """A context manager for `DmtxDecode`, created and destoyed by
   `dmtxDecodeCreate` and `dmtxDecodeDestroy`.

   Args:
      image (DmtxImage):
      shrink (int):

   Yields:
      DmtxDecode: The created image

   Raises:
      PyLibDMTXError: If the decoder could not be created.
   """
   decoder = dmtxDecodeCreate(image, shrink)
   if not decoder:
      raise PyLibDMTXError('Could not create decoder')
   else:
      try:
         yield decoder
      finally:
         dmtxDecodeDestroy(decoder)


@contextmanager
def libdmtx_region(decoder, timeout):
   """A context manager for `DmtxRegion`, created and destoyed by
   `dmtxRegionFindNext` and `dmtxRegionDestroy`.

   Args:
      decoder (DmtxDecode):
      timeout (int or None):

   Yields:
      DmtxRegion: The next region or None, if all regions have been found.
   """
   region = dmtxRegionFindNext(decoder, timeout)
   try:
      yield region
   finally:
      dmtxRegionDestroy(region)


@contextmanager
def libdmtx_decoded_matrix_region(decoder, region, corrections):
   """A context manager for `DmtxMessage`, created and destoyed by
   `dmtxDecodeMatrixRegion` and `dmtxMessageDestroy`.

   Args:
      decoder (DmtxDecode):
      region (DmtxRegion):
      corrections (int):

   Yields:
      DmtxMessage: The message.
   """
   message = dmtxDecodeMatrixRegion(decoder, region, corrections)
   try:
      yield message
   finally:
      dmtxMessageDestroy(message)


def decode(image, timeout=None, gap_size=None, shrink=1, shape=None,
           deviation=None, threshold=None, min_edge=None, max_edge=None,
           corrections=None, max_count=None):
   """Decodes datamatrix barcodes in `image`.

   Args:
      image: numpy.ndarray, PIL.Image or tuple (pixels, width, height)
      timeout (int): milliseconds
      gap_size (int):
      shrink (int):
      shape (int):
      deviation (int):
      threshold (int):
      min_edge (int):
      max_edge (int):
      corrections (int):
      max_count (int): stop after reading this many barcodes. `None` to read as
         many as possible.

   Yields:
      :obj:`list` of :obj:`Decoded`: The values decoded from barcodes.
   """
   dmtx_timeout = None
   if timeout:
      dmtx_timeout = dmtxTimeAdd(dmtxTimeNow(), timeout)

   if max_count is not None and max_count < 1:
      raise ValueError('Invalid max_count [{0}]'.format(max_count))

   # Test for PIL.Image and numpy.ndarray without requiring that cv2 or PIL
   # are installed.
   if 'PIL.' in str(type(image)):
      pixels = image.convert('RGB').tobytes()
      width, height = image.size[:2]
   elif 'numpy.ndarray' in str(type(image)):
      pixels = image.tobytes()
      height, width = image.shape[:2]
   else:
      # image should be a tuple (pixels, width, height)
      pixels, width, height = image

   with libdmtx_image(
         cast(pixels, c_ubyte_p), width, height, DmtxPackOrder.DmtxPack24bppRGB
      ) as img:
      with libdmtx_decoder(img, shrink) as decoder:
         properties = [
            (DmtxProperty.DmtxPropScanGap, gap_size),
            (DmtxProperty.DmtxPropSymbolSize, shape),
            (DmtxProperty.DmtxPropSquareDevn, deviation),
            (DmtxProperty.DmtxPropEdgeThresh, threshold),
            (DmtxProperty.DmtxPropEdgeMin, min_edge),
            (DmtxProperty.DmtxPropEdgeMax, max_edge)
         ]

         # Set only those properties with a non-False value
         for prop, value in filter(lambda v: v[1], properties):
            dmtxDecodeSetProp(decoder, prop, value)

         if not corrections:
            corrections = DmtxUndefined

         results = []
         while True:
            with libdmtx_region(decoder, dmtx_timeout) as region:
               # Finished file or ran out of time before finding another region
               if not region:
                  break

               with libdmtx_decoded_matrix_region(
                     decoder, region, corrections
                  ) as msg:
                  # Coordinates
                  p00 = DmtxVector2()
                  p11 = DmtxVector2(1.0, 1.0)
                  dmtxMatrix3VMultiplyBy(p00, region.contents.fit2raw)
                  dmtxMatrix3VMultiplyBy(p11, region.contents.fit2raw)
                  x0 = int((shrink * p00.X) + 0.5)
                  y0 = int((shrink * p00.Y) + 0.5)
                  x1 = int((shrink * p11.X) + 0.5)
                  y1 = int((shrink * p11.Y) + 0.5)
                  results.append(Decoded(
                     string_at(msg.contents.output),
                     Rect(x0, y0, x1 - x0, y1 - y0)
                  ))

            # Stop if we've reached maximium count
            if max_count and len(results) == max_count:
               break

   return results
