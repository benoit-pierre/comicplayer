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

import pygame
import pygame.locals as pyg

import math
import os
import traceback

from mcomix import image_tools
from mcomix import log
from mcomix.smart_scroller import Frame, Rect, SmartScroller
from mcomix.worker_thread import WorkerThread

from image import Image

from comic_book import BaseComicBook, ComicBook
from displayer_renderer import Renderer

class DisplayerApp:

    CURSOR_HIDE, CACHE_NEXT_PAGE = xrange(pygame.USEREVENT, pygame.USEREVENT + 2)

    VIEW_1_1, VIEW_WIDTH, VIEW_WIDEN_5_4 = xrange(3)
    ZOOM_IN, ZOOM_OFF, ZOOM_OUT = xrange(3)

    def __init__(self, comics):
        pygame.font.init()
        try:
            font = pygame.font.Font('resources'+os.sep+'DejaVuSansCondensed-Bold.ttf', 18)
        except IOError:
            font_name = pygame.font.get_default_font()
            font = pygame.font.Font(font_name, 18)
        pygame.display.init()
        self.scroller = SmartScroller()
        self.renderer = Renderer(pygame.display.get_surface(), font)
        disp_info = pygame.display.Info()
        self.display_width = disp_info.current_w
        self.display_height = disp_info.current_h
        self.fullscreen = True
        self.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(self.CURSOR_HIDE, 2000)

        self.cleaner_thread = WorkerThread(self.clean, max_threads=2)
        self.view_mode = self.VIEW_WIDEN_5_4
        self.zoom_mode = self.ZOOM_OFF
        self.zoom_lock = self.ZOOM_OFF
        self.disable_animations = True
        self.only_1_frame = False
        self.border_width = 16
        self.clipping = True
        self.previous_state = None
        self.state = "entering_page"
        self.flip_dir = True
        self.running = True
        self.progress = 0.0
        self.row_id = 0
        self.rows = []
        self.page_id = 0
        self.next_page_id = 0
        self.comic_id = 0
        self.next_comic_id = 0
        self.comics = comics
        self.comix = None
        self.load_comic(0)

    def clean(self, mess):
        comic, = mess
        log.debug('closing %s', comic.pretty_name)
        comic.close()

    def close_comic(self):
        comic = self.comix
        if comic is None:
            return
        self.comix = None
        self.cleaner_thread.append_order((comic,))

    def load_comic(self, comic_id):
        log.info('loading comic %u', comic_id)
        self.close_comic()
        try:
            comix = ComicBook(self.comics[comic_id])
        except Exception, e:
            msg = 'could not load comic %s: %s' % (self.comics[comic_id], e)
            log.debug('%s:\n%s', msg, traceback.format_exc())
            self.add_msg(msg, ttl=5)
            comix = None
        if comix is None:
            self.comix = BaseComicBook(self.comics[comic_id])
            self.pos = ((0,0,) + self.renderer.scrdim) * 3
            self.state = 'static'
            self.force_redraw = True
        else:
            self.comix = comix
        self.renderer.page = None
        self.comic_id = comic_id
        self.pages = {}
        if len(self.comix) > 0:
            if self.flip_dir:
                page_id = 0
            else:
                page_id = len(self.comix) - 1
            self.load_page(page_id)
        else:
            self.next_page_id = self.page_id = 0

    def prepare_page(self, page_id):

        if page_id in self.pages:
            view_mode, page, bgcolor, frames = self.pages.get(page_id)
            if view_mode == self.view_mode:
                return
            del self.pages[page_id]

        log.info('preparing page %u', page_id)

        name = self.comix.get_filename(page_id)
        fil = self.comix.get_file(page_id)

        image = Image.from_file(fil)
        width, height = image.size

        screen_width, screen_height = self.renderer.scrdim

        page_ratio = float(width) / height
        if page_ratio > 1.0:
            width, height = height, width
            screen_width, screen_height = screen_height, screen_width

        if self.VIEW_WIDEN_5_4 == self.view_mode:
            # widen to occupy 5:4 ratio zone on screen
            width_5_4 = (screen_height - 2 * self.border_width) * 5 / 4
            multiplier = 1.0*width_5_4 / width
            width2 = width_5_4
            height2 = int(math.floor(height * multiplier))
        elif self.VIEW_WIDTH == self.view_mode:
            # Match screen size.
            width2 = screen_width
            height2 = int(math.floor(1.0 * height * width2 / width))
        else:
            # Keep image native resolution.
            width2, height2 = width, height

        if page_ratio > 1.0:
            width, height = height, width
            width2, height2 = height2, width2
            screen_width, screen_height = screen_height, screen_width

        # Don't upscale.
        if width2 > width or height2 > height:
            width2, height2 = width, height
        elif width2 != width or height2 != height:
            image = image.resize((width2, height2))

        page = pygame.image.fromstring(image.to_rgb(), (width2, height2), "RGB")

        image = image.to_pil()
        page_bgcolor = self.comix.get_bgcolor(page_id)
        if page_bgcolor is None:
            log.info('detecting page %u background color', page_id)
            page_bgcolor = image_tools.get_most_common_edge_colour(image)
            self.comix.set_bgcolor(page_id, page_bgcolor)

        frames = self.comix.get_frames(page_id)
        if frames is None:
            log.info('detecting page %u frames', page_id)
            self.scroller.setup_image(image, page_bgcolor)
            page_frames = self.scroller._frames
            frames = []
            for f in page_frames:
                x = float(f.rect.x) / width2
                y = float(f.rect.y) / height2
                w = float(f.rect.w) / width2
                h = float(f.rect.h) / height2
                frames.append((x, y, w, h))
            self.comix.set_frames(page_id, frames)
        else:
            page_frames = []
            for x, y, w, h in frames:
                x = int(x * width2)
                y = int(y * height2)
                w = int(w * width2)
                h = int(h * height2)
                f = Frame(Rect(x, y, w, h), len(page_frames), None)
                page_frames.append(f)

        self.pages[page_id] = (self.view_mode, page, page_bgcolor, page_frames)

    def load_page(self, page_id, frame_number=None):
        log.info('loading page %u%s', page_id,
                 '' if frame_number is None else ' (frame %u)' % frame_number)
        self.prepare_page(page_id)
        view_mode, page, bgcolor, frames = self.pages[page_id]
        self.page_id = page_id
        self.renderer.page = page
        self.renderer.zoom_cache = {}
        self.progress = 0.0
        self.original_frames = frames
        self.renderer.set_background_color(bgcolor)
        self.find_rows(frame_number=frame_number)
        self.src_pos = self.pos = self.oid2pos(self.row_id)

    def find_rows(self, frame_number=None):

        self.row_id = 0
        self.scroller._frames = self.original_frames

        screen_width, screen_height = self.renderer.scrdim

        view_width = screen_width - 2 * self.border_width
        view_height = screen_height - 2 * self.border_width
        if self.zoom_mode == self.ZOOM_IN:
            self.scroller.setup_view(0, 0, view_width, view_height)

        row_frame_number = []
        rows = []
        fn = 0
        while fn < len(self.scroller._frames):
            f = self.scroller._frames[fn]
            if self.only_1_frame:
                self.scroller._view_x = 0
                self.scroller._view_y = 0
                self.scroller._view_width = f.rect.w
                self.scroller._view_height = f.rect.h
            elif self.zoom_mode != self.ZOOM_IN:
                self.scroller._view_x = 0
                self.scroller._view_y = 0
                self.scroller._view_width = max(f.rect.w, view_width)
                self.scroller._view_height = max(f.rect.h, view_height)
            x, y, w, h = self.scroller.scroll(to_frame=fn)
            bl = self.border_width
            br = self.border_width
            bt = self.border_width
            bb = self.border_width
            if f.split is None:
                cx, cy, cw, ch = x, y, w, h
            else:
                ff = self.original_frames[f.number]
                cx, cy, cw, ch = ff.rect
                if f.rect.x > ff.rect.x:
                    bl = 0
                if f.rect.y > ff.rect.y:
                    bt = 0
                if f.rect.x + f.rect.w < ff.rect.x + ff.rect.w:
                    br = 0
                if f.rect.y + f.rect.h < ff.rect.y + ff.rect.h:
                    bb = 0
            if self.only_1_frame or \
               w > screen_width or \
               h > screen_height:
                next_fn = fn + 1
            else:
                next_fn = self.scroller._current_frames[1] + 1
            frames = self.scroller._frames[fn:next_fn]
            if frame_number in [f.number for f in frames]:
                self.row_id = len(rows)
                frame_number = None
            row_frame_number.append(frames[0].number)
            rows.append((x, y, x + w - 1, y + h - 1,
                         cx, cy, cx + cw - 1, cy + ch - 1,
                         bl, bt, br, bb))
            fn = next_fn

        self.row_frame_number = row_frame_number
        self.rows = rows

    def reload_rows(self):
        fn = self.row_frame_number[self.row_id]
        self.find_rows(frame_number=fn)

    def reload_page(self):
        self.src_pos = self.pos
        self.state = 'leaving_page'

    def oid2pos(self, oid):
        if self.zoom_mode == self.ZOOM_OUT:
            w = self.renderer.page.get_width()
            h = self.renderer.page.get_height()
            return 2 * (0, 0, w - 1, h - 1) + 4 * (self.border_width,)
        return self.rows[oid]

    def zoom_out(self):
        self.zoom_mode = self.ZOOM_OUT
        self.src_pos = self.pos
        self.state = 'zooming'
        self.progress = 0.0

    def zoom_in(self):
        self.zoom_mode = self.ZOOM_IN
        self.reload_rows()
        self.state = 'zooming'
        self.progress = 0.0
        self.src_pos = self.pos

    def unzoom(self):
        self.zoom_mode = self.ZOOM_OFF
        self.reload_rows()
        self.src_pos = self.pos
        self.state = 'change_row'
        self.progress = 0.0

    def flip_comic(self, delta, rowwise=False):
        next_comic_id = self.comic_id + delta
        if next_comic_id < 0:
            next_comic_id = 0
        if next_comic_id >= len(self.comics):
            next_comic_id = len(self.comics) - 1
        if next_comic_id == self.comic_id:
            return
        self.next_comic_id = next_comic_id
        self.flip_dir = next_comic_id > self.comic_id
        self.flip_to_last = rowwise
        self.src_pos = self.pos
        self.state = "leaving_page"

    def flip_page(self, delta, rowwise=False):
        self.zoom_mode = self.zoom_lock
        next_comic_id = self.comic_id
        nci = self.page_id
        nci += delta
        if nci<0:
            if -1 == delta:
                return self.flip_comic(-1, rowwise=rowwise)
            nci = 0
        elif nci>=len(self.comix):
            if 1 == delta:
                return self.flip_comic(+1, rowwise=rowwise)
            nci = len(self.comix)-1
            if nci < 0:
                nci = 0

        if nci == self.page_id:
            return
        self.next_page_id = nci
        self.flip_dir = nci > self.page_id
        self.flip_to_last = rowwise
        self.src_pos = self.pos
        self.state = "leaving_page"

    def navigate_row(self, delta, force=False):
        if self.zoom_mode == self.ZOOM_OUT:
            self.flip_page(delta)
            return
        oid = self.row_id
        oid += delta
        if oid<0:
            self.flip_page(-1,True)
            return
        if oid>=len(self.rows):
            self.flip_page(+1)
            return
        if force or self.row_id!=oid:
            self.row_id = oid
            self.progress = 0.0
            self.src_pos = self.pos
            self.state = "change_row"

    def shifted_page(self, forward = False):
        if self.disable_animations:
            return self.pos
        x0,y0,x1,y1 = self.pos[0:4]
        cx0,cy0,cx1,cy1 = self.pos[4:8]
        w,h = self.renderer.scrdim
        ch = self.renderer.page.get_height()

        if forward:
            shift = -h
        else:
            shift = ch
        y0 += shift
        y1 += shift
        cy0 += shift
        cy1 += shift
        return (x0,y0,x1,y1,cx0,cy0,cx1,cy1)+tuple(self.pos[8:12])

    def start_load_page(self):
        reload = self.next_comic_id == self.comic_id and self.next_page_id == self.page_id
        log.info('start loading page %u (reload? %s)', self.next_page_id,
                 'yes' if reload else 'no')
        if reload:
            fn = self.row_frame_number[self.row_id]
            self.load_page(self.next_page_id, frame_number=fn)
        else:
            if self.next_comic_id != self.comic_id:
                self.load_comic(self.next_comic_id)
            else:
                self.load_page(self.next_page_id)
            if not self.flip_dir and self.flip_to_last:
                self.row_id = len(self.rows)-1
            else:
                self.row_id = 0
        self.target_pos = self.oid2pos(self.row_id)
        self.pos = self.target_pos
        self.src_pos = self.shifted_page(self.flip_dir)
        self.pos = self.src_pos

    def cache_next_page(self):
        for page_id in self.pages.keys():
            if abs(page_id - self.page_id) > 1:
                del self.pages[page_id]
        step = +1 if self.flip_dir else -1
        page_id = self.page_id + step
        if 0 <= page_id and page_id < len(self.comix):
            self.prepare_page(page_id)
        log.info('page cache: %s', [page_id for page_id in self.pages])
        assert len(self.pages) <= 3

    def end_changing_page(self):
        pygame.event.post(pygame.event.Event(self.CACHE_NEXT_PAGE))

    def add_msg(self, text, ttl=1.5):
        color = pygame.color.Color(*self.renderer.bg)
        color.hsla = (color.hsla[0], color.hsla[1], 100 - color.hsla[2], color.hsla[3])
        text = self.renderer.font.render(text, True, color, self.renderer.bg)
        self.renderer.textimages.append([text,255,ttl])

    def show_help(self):
        self.state = 'help'
        self.renderer.show_help()

    def show_info(self):
        if 0 == len(self.comix):
            msg = '%s' % self.comix.path
        else:
            msg = '%s - %u/%u - %s - %ux%u' % (
                self.comix.pretty_name,
                self.page_id + 1,
                len(self.comix),
                self.comix.get_filename(self.page_id),
                self.renderer.page.get_width(),
                self.renderer.page.get_height(),
            )
        self.add_msg(msg, ttl=2)

    states = {
        "change_row": {
            "motion": True,
            "target": lambda self: self.oid2pos(self.row_id),
            "changeto": "static"
        },
        "zooming": {
            "motion": True,
            "target": lambda self: self.oid2pos(self.row_id),
            "changeto": "zoomed"
        },
        "leaving_page": {
            "motion": True,
            "target": lambda self: self.shifted_page(not self.flip_dir),
            "changeto": "entering_page",
            "onfinish": start_load_page,
        },
        "entering_page": {
            "motion": True,
            "target": lambda self: self.oid2pos(self.row_id),
            "changeto": "static",
            "onfinish": end_changing_page,
        },
        "static": {
            "motion": False,
            "changeto": "static",
        },
        "zoomed": {
            "motion": False
        },
        "help": {
            "motion": False
        }
    }

    input_bindings = {
        'mouse1'         : ('navigate', +1),
        'mouse3'         : ('navigate', -1),
        'mouse2'         : ('lock_zoom', None),
        'mouse4'         : ('set_zoom', 'in'),
        'mouse5'         : ('set_zoom', 'out'),
        'f'              : ('toggle_fullscreen', None),
        'w'              : ('set_view', VIEW_WIDTH),
        'a'              : ('set_view', VIEW_1_1),
        's'              : ('set_view', VIEW_WIDEN_5_4),
        'escape'         : ('quit', None),
        'q'              : ('quit', None),
        'return'         : ('toggle_zoom', None),
        'f1'             : ('help', None),
        'f2'             : ('toggle_animations', None),
        'f3'             : ('toggle_only_1_frame', None),
        'f4'             : ('toggle_clipping', None),
        'left'           : ('flip_page', -1),
        'shift+left'     : ('flip_page', -5),
        'ctrl+left'      : ('flip_page', -20),
        'right'          : ('flip_page', +1),
        'shift+right'    : ('flip_page', +5),
        'ctrl+right'     : ('flip_page', +20),
        'page up'        : ('set_zoom', 'in'),
        'page down'      : ('set_zoom', 'out'),
        'shift+page up'  : ('flip_comic', -1),
        'shift+page down': ('flip_comic', +1),
        'end'            : ('lock_zoom', None),
        'up'             : ('navigate', -1),
        'down'           : ('navigate', +1),
        'backspace'      : ('navigate', -1),
        'space'          : ('navigate', +1),
        'tab'            : ('show_info', None),
    }

    def quit(self):
        self.running = False

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            pygame.display.set_mode((self.display_width,self.display_height), pyg.HWSURFACE|pyg.DOUBLEBUF|pyg.FULLSCREEN)
        else:
            pygame.display.set_mode((1280,1024), pyg.HWSURFACE|pyg.DOUBLEBUF)
        self.renderer.set_screen(pygame.display.get_surface())

    def process_action(self, action, arg=None):
        if self.state == 'help':
            if action in ('help', 'quit'):
                self.state = 'change_row'
                self.progress = 1
        elif action == 'quit':
            self.quit()
        elif action == 'help':
            self.show_help()
            self.force_redraw = False
        elif action == 'hide_cursor':
            pygame.mouse.set_visible(False)
            pygame.time.set_timer(self.CURSOR_HIDE, 0)
        elif action == 'show_cursor':
            pygame.mouse.set_visible(True)
            pygame.time.set_timer(self.CURSOR_HIDE, 2000)
        elif action == 'cache_next_page':
            self.cache_next_page()
        elif action == 'toggle_zoom':
            if self.zoom_mode == self.ZOOM_OFF:
                self.zoom_out()
            elif self.zoom_mode == self.ZOOM_OUT:
                self.zoom_in()
            elif self.zoom_mode == self.ZOOM_IN:
                self.unzoom()
        elif action == 'lock_zoom':
            self.zoom_lock = self.zoom_mode
        elif action == 'set_zoom':
            if self.zoom_mode == self.ZOOM_OFF:
                if arg == 'in':
                    self.zoom_in()
                elif arg == 'out':
                    self.zoom_out()
            else:
                self.unzoom()
        elif action == 'navigate':
            if self.state not in ['leaving_page']:
                self.navigate_row(arg)
        elif action == 'toggle_fullscreen':
            self.toggle_fullscreen()
            self.reload_page()
        elif action == 'set_view':
            if arg != self.view_mode:
                self.view_mode = arg
                self.reload_page()
        elif action == 'redraw':
            self.force_redraw = True
        elif action == 'toggle_animations':
            self.disable_animations = not self.disable_animations
        elif action == 'toggle_only_1_frame':
            self.only_1_frame = not self.only_1_frame
            self.reload_page()
        elif action == 'toggle_clipping':
            self.clipping = not self.clipping
            self.force_redraw = True
        elif action == 'flip_page':
            if self.state not in ['leaving_page']:
                self.flip_page(arg)
        elif action == 'flip_comic':
            if self.state not in ['leaving_comic']:
                self.flip_comic(arg)
        elif action == 'show_info':
            self.show_info()
        else:
            log.error('invalid action: %s(%s)', action, arg)

    def process_event(self, event):
        action, arg = None, None
        if event.type == pyg.QUIT:
            action = 'quit'
        elif event.type == self.CURSOR_HIDE:
            action = 'hide_cursor'
        elif event.type == pyg.MOUSEMOTION:
            action = 'show_cursor'
        elif event.type == pyg.VIDEOEXPOSE:
            action = 'redraw'
        elif event.type == self.CACHE_NEXT_PAGE:
            action = 'cache_next_page'
        elif event.type == pyg.KEYDOWN:
            input = pygame.key.name(event.key)
            if event.mod & pyg.KMOD_SHIFT:
                input = 'shift+' + input
            if event.mod & pyg.KMOD_CTRL:
                input = 'ctrl+' + input
            if event.mod & pyg.KMOD_ALT:
                input = 'alt+' + input
            if input in self.input_bindings:
                action, arg = self.input_bindings[input]
        elif event.type == pyg.MOUSEBUTTONUP:
            input = 'mouse%u' % event.button
            if input in self.input_bindings:
                action, arg = self.input_bindings[input]
        if action is not None:
            self.process_action(action, arg)

    def update_screen(self, msec):
        if self.previous_state != self.state:
            log.info('update_screen: %s -> %s', self.previous_state, self.state)
            self.previous_state = self.state
        if self.state=='help':
            return
        motion = self.states[self.state]["motion"]
        if motion or self.force_redraw or len(self.renderer.textimages)>0:
            if motion:
                self.progress += 0.0050*msec
                if self.disable_animations:
                    self.progress = 1
                    motion = False

                target_pos = self.states[self.state]["target"](self)
                if self.progress>=1:
                    self.progress = 1
                    if "onfinish" in self.states[self.state]:
                        self.states[self.state]["onfinish"](self)
                        self.clock.tick(50) # transition should not take progress time
                    else:
                        self.pos = target_pos
                    self.state = self.states[self.state]["changeto"]
                    self.progress = 0
                    motion = False
                else:
                    pos = [0]*len(target_pos)
                    p2 = (1-math.cos(math.pi*self.progress))/2
                    for i in xrange(len(target_pos)):
                        pos[i] = int(self.src_pos[i]*(1.0-p2) + target_pos[i]*p2)
                    self.pos = pos
            for ti in self.renderer.textimages:
                ti[2] -= msec/1000.0
                if ti[2]<0:
                    ti[1] = 255+255*2*ti[2]
            self.renderer.textimages = [ti for ti in self.renderer.textimages if ti[1]>0]

            self.renderer.render(self.pos, motion, clipping=self.clipping)

    def loop(self, events):
        msec = self.clock.tick(50)
        self.force_redraw = False
        for event in events:
            self.process_event(event)
        self.update_screen(msec)

    def run(self):
        try:
            while self.running:
                self.loop(pygame.event.get())
        finally:
            self.close_comic()
            self.cleaner_thread.stop(finish=True)
            pygame.quit()

if __name__=="__main__":
    try:
        import debug_scripts
    except ImportError:
        debug_scripts = False
    if debug_scripts:
        debug_scripts.go()

