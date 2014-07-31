
import os.path

from mcomix import archive

import py7zlib

class SevenZipArchive(archive.archive_base.BaseArchive):

    def __init__(self, archive):
        self._archive = py7zlib.Archive7z(open(archive))

    def list_contents(self):
        return self._archive.filenames

    def extract(self, filename, destination_dir):
        assert isinstance(filename, unicode) and \
            isinstance(destination_dir, unicode)

        print 'extract(%s)' % filename
        data = self._archive.getmember(filename)
        new = self._create_file(os.path.join(destination_dir, filename))
        new.write(data.read())
        new.close()

    def is_solid(self):
        return self._archive.solid

