
from base_image import BaseImage

from libs import gm_wrap

import ctypes
import sys

gm_wrap.InitializeMagick(sys.argv[0])
_exception = ctypes.pointer(gm_wrap.ExceptionInfo())
gm_wrap.GetExceptionInfo(_exception)

class GraphicsMagicImage(BaseImage):

    def __init__(self, image):
        self._image = image

    def __del__(self):
        gm_wrap.DestroyImage(self._image)

    @property
    def size(self):
        return (self._image.contents.columns, self._image.contents.rows)

    def to_rgb(self):
        width, height = self.size
        buffer = ctypes.create_string_buffer(width * height * 3)
        gm_wrap.DispatchImage(self._image, 0, 0, width, height, 'RGB', gm_wrap.CharPixel, buffer, _exception)
        return buffer.raw

    def resize(self, size, fast=False):
        if fast:
            filter = gm_wrap.CubicFilter
        else:
            filter = gm_wrap.LanczosFilter
        return GraphicsMagicImage(gm_wrap.ResizeImage(self._image, size[0], size[1], filter, 1, _exception))

    def save(self, filename):
        image_info = gm_wrap.CloneImageInfo(None)
        self._image.contents.filename = filename
        gm_wrap.WriteImage(image_info, self._image)
        gm_wrap.DestroyImageInfo(image_info)

    @classmethod
    def open(self, filename):
        image_info = gm_wrap.CloneImageInfo(None)
        image_info.contents.filename = filename
        image = GraphicsMagicImage(gm_wrap.ReadImage(image_info, _exception))
        gm_wrap.DestroyImageInfo(image_info)
        return image

    @classmethod
    def from_string(self, string):
        image_info = gm_wrap.CloneImageInfo(None)
        image = GraphicsMagicImage(gm_wrap.BlobToImage(image_info, string, len(string), _exception))
        gm_wrap.DestroyImageInfo(image_info)
        return image

