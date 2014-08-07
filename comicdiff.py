#!/usr/bin/env python2

import threading
import sys
import os

from collections import namedtuple

from libs.comic_book import MComixBook
from libs.image import Image
from mcomix import archive_tools, constants, portability
from mcomix.worker_thread import WorkerThread

COMIC_FORMATS = {
    constants.BZIP2       : 'tar/bzip2',
    constants.GZIP        : 'tar/gzip',
    constants.LHA         : 'lha',
    constants.PDF         : 'pdf',
    constants.RAR         : 'rar',
    constants.SEVENZIP    : '7z',
    constants.TAR         : 'tar',
    constants.ZIP         : 'zip',
    constants.ZIP_EXTERNAL: 'zip',
}

PageInfo = namedtuple('PageInfo', 'number name format resolution')
ComicInfo = namedtuple('ComicInfo', 'path name format size pages')
ComicInfo.__len__ = lambda self: len(self.pages)

def comic_info(path):

    comic = MComixBook(path)
    try:

        pages = []

        for n in xrange(len(comic)):
            page_name = comic.get_filename(n)
            format = os.path.splitext(page_name)[1][1:]
            image_data = comic.get_file(n).read()
            image = Image.from_string(image_data)
            width, height = image.size
            size = len(image_data)
            page_info = PageInfo(n, page_name, format, (width, height))
            pages.append(page_info)

        name = os.path.splitext(comic.pretty_name)[0]
        format = COMIC_FORMATS[archive_tools.archive_mime_type(path)]
        size = os.path.getsize(path)

        info = ComicInfo(path, name, format, size, pages)

        return info

    finally:
        comic.close()

def show_diff(name, f1, diff, f2, extra=None):
    fmt = '%-30s: %-30s %-2s %+30s'
    args = (name, f1, diff, f2)
    if extra is not None:
        fmt += ' [%s]'
        args = args + (extra,)
    print fmt % args

def format_size(s):
    for order, unit in (
        (0x40000000, 'G'),
        (0x00100000, 'M'),
        (0x00000400, 'K'),
    ):
        if 0 != s / order:
            return '%.2f%s' % (float(s) / order, unit)
    return '%u' % s

def show_diff_size(name, s1, s2):
    delta = s2 - s1
    s1 = format_size(s1)
    s2 = format_size(s2)
    delta = ('-' if delta < 0 else '+') + format_size(abs(delta))
    show_diff(name, s1, '<' if s1 < s2 else '>', s2, delta)

def show_diff_number(name, n1, n2):
    delta = n2 - n1
    show_diff(name, n1, '<' if n1 < n2 else '>', n2, '%+d' % delta)

def show_diff_string(name, s1, s2):
    show_diff(name, s1, '!=', s2)

def average_resolution(pages):
    width = sum([p.resolution[0] for p in pages])
    height = sum([p.resolution[1] for p in pages])
    return (width / len(pages), height / len(pages))

verbose = False

args = portability.get_commandline_args()

if '-v' == args[0]:
    verbose = True
    args.pop(0)

if 2 != len(args):
    sys.exit(2)

comics = {}
lock = threading.Lock()

def worker(path):
    info = comic_info(path)
    with lock:
        comics[path] = info

worker = WorkerThread(worker, max_threads=2)
worker.extend_orders(args)
try:
    worker.stop(finish=True)
finally:
    worker.stop()
comic1, comic2 = comics[args[0]], comics[args[1]]

lower_resolution = True
higher_resolution = True

num_common_pages = min(len(comic1), len(comic2))

num_page_diffs = 0
for n in xrange(num_common_pages):
    name = 'Page %u ' % n
    p1 = comic1.pages[n]
    p2 = comic2.pages[n]
    if p1 != p2:
        num_page_diffs += 1
    if p1.name != p2.name and verbose:
        show_diff_string(name + 'name', p1.name, p2.name)
    if p1.resolution != p2.resolution:
        w1, h1 = p1.resolution
        w2, h2 = p2.resolution
        if w1 >= w2 and h1 >= h2 or w1 <= w2 and h1 <= h2:
            if w1 >= w2:
                lower_resolution = False
                diff = '>'
            else:
                higher_resolution = False
                diff = '<'
            r1 = '%ux%u' % (w1, h1)
            r2 = '%ux%u' % (w2, h2)
            if verbose:
                show_diff(name + 'resolution', r1, diff, r2)
        elif verbose:
            show_diff_number(name + 'width', w1, w2)
            show_diff_number(name + 'height', h1, h2)

comic_diff = 0
if comic1.name != comic2.name:
    comic_diff += 1
    show_diff_string('Name', comic1.name, comic2.name)
if comic1.format != comic2.format:
    comic_diff += 1
    show_diff_string('Format', comic1.format, comic2.format)
if comic1.size != comic2.size:
    comic_diff += 1
    show_diff_size('Size', comic1.size, comic2.size)
if len(comic1) != len(comic2):
    comic_diff += 1
    show_diff_number('Length', len(comic1), len(comic2))
if 0 != num_page_diffs:
    comic_diff += 1
    print '%-30s: %-30s %-2s %+30s' % ('Different pages', num_page_diffs, '/', num_common_pages)
if lower_resolution != higher_resolution:
    comic_diff += 1
    r1 = '~%ux%u' % average_resolution(comic1.pages[:num_common_pages])
    r2 = '~%ux%u' % average_resolution(comic2.pages[:num_common_pages])
    show_diff('Resolution', r1, '<' if lower_resolution else '>', r2)

sys.exit(0 if 0 == comic_diff else 1)

