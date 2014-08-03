#!/usr/bin/env python2

import argparse
import copy
import os
import pdb
import re
import shutil
import subprocess
import sys
import tempfile
import traceback

from mcomix.image_tools import get_most_common_edge_colour
from mcomix.smart_scroller import SmartScroller

from libs.comic_book import MComixBook
from libs.image import Image

print Image

def display(value):
    m = re.match('^(\d+)x(\d+)$', value)
    if not m:
        raise argparse.ArgumentError()
    width, height = int(m.group(1)), int(m.group(2))
    return (width, height)

parser = argparse.ArgumentParser(prog='comic2acv')
parser.add_argument('-d', '--display', type=display,
                    dest='display', metavar='WIDTHxHEIGHT', default=None,
                    help='target display size (will downscale to match if used)')
parser.add_argument('-D', '--downscale', type=int,
                    dest='downscale', metavar='SIZE', default=None,
                    help='will downscale images to under SIZExSIZE')
parser.add_argument('-o', '--output',
                    dest='output', metavar='FILE', default=None,
                    help='output file path')
parser.add_argument('comic', nargs=1, help='path to comic archive to convert')

options = parser.parse_args(sys.argv[1:])
options.comic = unicode(options.comic[0])

if options.output is None:
    base, ext = os.path.splitext(options.comic)
    options.output = base + '.acv'

if os.path.exists(options.output):
    print >>sys.stderr, 'output already exists: %s' % options.output
    sys.exit(1)

cleanup = []
try:

    scroller = SmartScroller()

    tmpdir = tempfile.mkdtemp(prefix=u'comic2acv.')
    cleanup.append(lambda: shutil.rmtree(tmpdir, True))

    comic = MComixBook(options.comic)
    cleanup.append(comic.close)

    if 0 == len(comic):
        print >>sys.stderr, 'no images found in comic: %s' % options.comic
        sys.exit(2)

    acv_xml = open(os.path.join(tmpdir, 'acv.xml'), 'wb')
    cleanup.append(acv_xml.close)
    acv_xml.write('<comic>\n')

    manifest_path = os.path.join(tmpdir, 'manifest')
    manifest = open(manifest_path, 'w+b')
    cleanup.append(manifest.close)
    manifest.write(os.path.join(tmpdir, 'acv.xml') + '\n')

    for n in xrange(len(comic)):
        print 'processing page %u: %s' % (n, comic.get_filename(n))
        image_path = os.path.join(tmpdir, comic.get_filename(n))
        image_data = comic.get_file(n).read()
        image = Image.from_string(image_data)
        width, height = image.size

        if options.downscale:
            max_size = options.downscale
            if width > max_size:
                height *= float(max_size) / width
                width = max_size
            if height > max_size:
                width *= float(max_size) / height
                height = max_size
            width = int(round(width))
            height = int(round(height))

        if (width, height) != image.size:
            print 'downscaling image from %ux%u to %ux%u' % (
                image.size[0], image.size[1], width, height)
            image = image.resize((width, height))

        image.save(image_path)

        if options.display:
            view_width, view_height = options.display
        else:
            view_width, view_height = 0, 0

        manifest.write(image_path + '\n')

        pil_image = image.to_pil()
        bgcolor = get_most_common_edge_colour(pil_image)
        scroller.setup_image(pil_image, bgcolor)
        acv_xml.write(' <screen index="%u" bgcolor="#%02x%02x%02x">\n' % (n,
                                                                          bgcolor[0],
                                                                          bgcolor[1],
                                                                          bgcolor[2]))
        fn = 0
        while fn < len(scroller._frames):
            f = scroller._frames[fn]
            scroller._view_x = 0
            scroller._view_x = 0
            scroller._view_width = max(f.rect.w, view_width)
            scroller._view_height = max(f.rect.h, view_height)
            pos = scroller.scroll(to_frame=fn)
            x, y, w, h = pos
            if x < 0:
                w += x
                x = 0
            if x + w > width:
                w = width - x
            if y < 0:
                h += y
                y = 0
            if y + h > height:
                h = height - y
            x = float(x) / width
            y = float(y) / height
            w = float(w) / width
            h = float(h) / height
            acv_xml.write('  <frame relativeArea="%f %f %f %f"/>\n' % (x, y, w, h))
            fn = scroller._current_frames[1] + 1
        acv_xml.write(' </screen>\n')
    acv_xml.write('</comic>\n')
    acv_xml.close()

    manifest.seek(0)

    print 'creating final %s' % options.output
    retcode = subprocess.call(['zip', '-9', options.output,
                               '--junk-path', '-@'],
                              stdin=manifest)
    if 0 != retcode:
        sys.exit(retcode)

finally:
    # print traceback.format_exc()
    # pdb.post_mortem()
    for fn in reversed(cleanup):
        fn()
