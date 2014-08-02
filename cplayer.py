#!/usr/bin/env python2
# coding: UTF-8

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

from libs.comic_book import ComicBook
import libs.displayer

import sys, os

from mcomix import log

if sys.platform=="win32":
    running_from_source = True
    os.environ["MAGICK_CODER_MODULE_PATH"]="."
    try:
        os.chdir("building_on_windows\\dlls")
    except OSError:
        running_from_source = False
    import libs.gm_wrap_win as gm_wrap
    libs.displayer.init_gm(gm_wrap)
    if running_from_source:
        os.chdir("..")
else:
    import libs.gm_wrap as gm_wrap
    libs.displayer.init_gm(gm_wrap)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.exit(1)
    if '-d' == sys.argv[1]:
        log.setLevel(log.DEBUG)
        sys.argv.pop(0)
    for n, path in enumerate(sys.argv[1:]):
        comic = ComicBook(path)
        if comic is None:
            print >>sys.stderr, 'could not load %s' % path
            continue
        try:
            dapp = libs.displayer.DisplayerApp(comic)
            dapp.run()
        finally:
            comic.close()

