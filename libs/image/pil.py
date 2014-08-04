
from base_image import BaseImage

from PIL import Image
from io import BytesIO

class PILImage(BaseImage):

    def __init__(self, image):
        self._image = image
        self._image.load()

    @property
    def size(self):
        return self._image.size

    def to_rgb(self):
        image = self._image
        if 'RGB' != image.mode:
            image = image.convert('RGB')
        return image.tostring()

    def crop(self, box, fast=False):
        return PILImage(self._image.crop(box))

    def resize(self, size, fast=False):
        if fast:
            resample = Image.NEAREST
        else:
            resample = Image.ANTIALIAS
        return PILImage(self._image.resize(size, resample))

    def save(self, filename):
        self._image.save(filename)

    def to_pil(self):
        return self._image

    @classmethod
    def open(self, filename):
        return PILImage(Image.open(filename))

    @classmethod
    def from_rgb(self, string, size):
        return PILImage(Image.frombuffer('RGB', size, string, 'raw', 'RGB', 0, 1))

    @classmethod
    def from_string(self, string):
        return PILImage.open(BytesIO(string))

    @classmethod
    def from_file(self, file):
        return PILImage.open(file)

