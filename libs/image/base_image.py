
class BaseImage():

    def __init__(self):
        pass

    @property
    def size(self):
        pass

    def to_rgb(self):
        pass

    def crop(self, box, fast=False):
        pass

    def resize(self, size, fast=False):
        pass

    def save(self, filename):
        pass

    def to_pil(self):
        from libs.image.pil import PILImage
        return PILImage.from_rgb(self.to_rgb(), self.size)._image

    @classmethod
    def open(self, filename):
        return self.from_file(open(filename, 'rb'))

    @classmethod
    def from_rgb(self, string, size):
        pass

    @classmethod
    def from_string(self, string):
        pass

    @classmethod
    def from_file(self, file):
        return self.from_string(file.read())

