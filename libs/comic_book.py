#   Copyright (c) 2009-2011, Konstantin Yegupov
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without modification,
#   are permitted provided that the following conditions are met:
#
#       * Redistributions of source code must retain the above copyright notice,
#         this list of conditions and the following disclaimer.
#
#       * Redistributions in binary form must reproduce the above copyright notice,
#         this list of conditions and the following disclaimer in the documentation
#         and/or other materials provided with the distribution.
#
#       * The name of the author may not be used to endorse or promote products
#         derived from this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#   ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#   (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#   LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#   ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os, os.path
import threading
import tempfile
import shutil
import glob
import re

from xml.etree import ElementTree

from mcomix.archive_tools import get_recursive_archive_handler, archive_mime_type
from mcomix.worker_thread import WorkerThread
from mcomix.tools import alphanumeric_sort
from mcomix import log

img_extensions = ['jpeg', 'jpg', 'gif', 'png']

class UnsupportedFileTypeError:
    pass

def ComicBook(path):
    if not os.path.isfile(path):
        if os.path.isdir(path):
            return DirComicBook(path)
        raise ValueError('invalid file path')
    else:
        if archive_mime_type(path) is not None:
            return MComixBook(unicode(path))
        ext = os.path.splitext(path)[1].lower()[1:]
        if ext in img_extensions:
            return SingleFileComicBook(path)
        else:
            raise UnsupportedFileTypeError('unsupported file type')

class BaseComicBook:

    def __init__(self, path):
        self.path = path
        self.filenames = []
        self._comic_bgcolor = None
        self._page_bgcolor = {}
        self._page_frames = {}

    def close(self):
        pass

    @property
    def pretty_name(self):
        return self.path.split(os.sep)[-1]

    def __len__(self):
        return len(self.filenames)

    def get_filename(self, page):
        return os.path.split(self.filenames[page])[1]

    def get_file(self, page):
        return self.get_file_by_name(self.filenames[page])

    def get_frames(self, page):
        return self._page_frames.get(page)

    def get_bgcolor(self, page):
        return self._page_bgcolor.get(page, self._comic_bgcolor)

    def set_frames(self, page, frames):
        self._page_frames[page] = frames

    def set_bgcolor(self, page, bgcolor):
        self._page_bgcolor[page] = bgcolor

class DirComicBook(BaseComicBook):

    def __init__(self, path):
        BaseComicBook.__init__(self, path)
        mask = os.path.join(os.path.normpath(path), '*')
        namelist = [fn[len(mask)-1:] for fn in glob.glob(mask)]
        self.filenames = [fn for fn in namelist if os.path.splitext(fn)[1][1:].lower() in img_extensions]
        alphanumeric_sort(self.filenames)

    def get_file_by_name(self, name):
        return open(os.path.join(self.path, name), 'rb')

class SingleFileComicBook(BaseComicBook):

    def __init__(self, path):
        BaseComicBook.__init__(self, path)
        self.filenames = [path]

    def get_file_by_name(self, name):
        basepath, simple_name = os.path.split(self.filenames[0])
        if name==self.filenames[0] or name==simple_name:
            return open(self.filenames[0], 'rb')
        else:
            return open(self.filenames[0]+"_"+name, 'rb')

class MComixBook(BaseComicBook):

    def __init__(self, path):
        BaseComicBook.__init__(self, path)
        self._tmpdir = tempfile.mkdtemp(prefix=u'comicplayer.')
        self._archive = get_recursive_archive_handler(path, self._tmpdir)
        self.filenames = []
        for f in self._archive.list_contents():
            if f == 'acv.xml':
                self._parse_acv(f)
                continue
            ext = os.path.splitext(f)[1].lower()[1:]
            if ext in img_extensions:
                self.filenames.append(f)
        alphanumeric_sort(self.filenames)
        self._condition = threading.Condition()
        self._extracted = set()
        if self._archive.support_concurrent_extractions:
            max_threads = 2
        else:
            max_threads = 1
        self._extract_thread = WorkerThread(self._extract,
                                            unique_orders=True,
                                            max_threads=max_threads)
        self._extract_all(0)

    def close(self):
        self._extract_thread.stop()
        self._archive.close()
        shutil.rmtree(self._tmpdir, True)

    def _parse_bgcolor(self, color):
        if not re.match('^#[0-9a-fA-F]{6}$', color):
            return None
        bgcolor = (int(color[1:3], 16),
                   int(color[3:5], 16),
                   int(color[5:7], 16))
        return bgcolor

    def _parse_acv(self, name):
        log.info('parsing ACV: %s', name)
        self._archive.extract(name, self._tmpdir)
        tree = ElementTree.parse(os.path.join(self._tmpdir, name))
        comic = tree.getroot()
        if 'comic' != comic.tag:
            log.error('ACV parser: root element is not comic: %s', comic.tag)
            return
        comic_bgcolor = None
        if 'bgcolor' in comic.attrib:
            bgcolor = self._parse_bgcolor(comic.attrib['bgcolor'])
            if bgcolor is None:
                log.error('invalid comic bgcolor: %s', comic.attrib['bgcolor'])
                return
            comic_bgcolor = bgcolor
        page_frames = {}
        page_bgcolor = {}
        for screen in comic:
            if 'screen' != screen.tag:
                continue
            if not 'index' in screen.attrib:
                log.error('screen has no index attribute')
                return
            page_number = int(screen.attrib['index'])
            if page_number in page_frames:
                log.error('duplicate screen %u', page_number)
                return
            if 'bgcolor' in screen.attrib:
                bgcolor = self._parse_bgcolor(screen.attrib['bgcolor'])
                if bgcolor is None:
                    log.error('invalid screen bgcolor: %s', screen.attrib['bgcolor'])
                    return
                page_bgcolor[page_number] = bgcolor
            frame_list = []
            for frame in screen:
                if 'frame' != frame.tag:
                    continue
                if not 'relativeArea' in frame.attrib:
                    log.error('frame has no relativeArea attribute')
                    return
                area = frame.attrib['relativeArea'].split()
                if 4 != len(area):
                    log.error('invalid frame relativeArea: %s', frame.attrib['relativeArea'])
                    return
                area = [float(f) for f in area]
                for f in area:
                    if f < 0.0 or f > 1.0:
                        log.error('invalid frame relativeArea: %s', frame.attrib['relativeArea'])
                        return
                frame_list.append(area)
            page_frames[page_number] = frame_list
        self._comic_bgcolor = comic_bgcolor
        self._page_bgcolor = page_bgcolor
        self._page_frames = page_frames

    def _extract_all(self, priority_index):
        self._extract_thread.clear_orders()
        priority_files = []
        for r in (
            (priority_index, 2),
            (priority_index - 1, 1),
            (priority_index + 2, len(self.filenames))
        ):
          s, l = r
          if s >= len(self.filenames):
              continue
          if s < 0:
              l += s
              s = 0
          if l + s > len(self.filenames):
              l = len(self.filenames) - s
          if l <= 0:
              continue
          for name in self.filenames:
              if not name in self._extracted:
                  priority_files.append(name)
        self._extract_thread.extend_orders(priority_files)

    def _extract(self, name):
        self._archive.extract(name, self._tmpdir)
        with self._condition:
            self._extracted.add(name)
            self._condition.notify()

    def get_file_by_name(self, name):
        priority_index = self.filenames.index(name)
        with self._condition:
            self._extract_all(priority_index)
            while not name in self._extracted:
                self._condition.wait()
        return open(os.path.join(self._tmpdir, name), 'rb')

