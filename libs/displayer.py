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
try:
    import pygame._view # required for cx_freeze to work
except ImportError:
    pass

import math
import sys, os, ctypes

from mcomix import image_tools, smart_scroller

from PIL import Image

from displayer_renderer import Renderer
import detect_rows

gm_wrap = None # to be supplied from main script

def init_gm(gm_wrap_module):
    global gm_wrap, exception
    gm_wrap = gm_wrap_module
    gm_wrap.InitializeMagick(sys.argv[0])
    exception = ctypes.pointer(gm_wrap.ExceptionInfo())
    gm_wrap.GetExceptionInfo(exception)
    

class FakeImage:
    def __init__(self, strdata, size):
        self.size = size
        self.strdata = strdata
    def tostring(self):
        return self.strdata

def rect_center(r):
    return [(r[0]+r[2])/2, (r[1]+r[3])/2]

def xy_range(xy1, xy2):
    return (xy2[0]-xy1[0])**2 + (xy2[1]-xy1[1])**2

def xy_rhombic_range(xy1, xy2):
    return abs(xy2[0]-xy1[0]) + abs(xy2[1]-xy1[1])

def row_merger(rows, scr_hei):
    # helper function to merge small rows into comfortably-sized ones
    old = rows[0]
    for new in rows[1:]:
        if new[1]-old[0]<scr_hei*0.8:
            old = (old[0], new[1], old[2])
        else:
            yield old
            old = new
    yield old

class DisplayerApp:
    def __init__(self, comix, callback=None, denoise_jpeg=True, ignore_small_rows=True):
        assert gm_wrap!=None, "GraphicsMagick not loaded"
        pygame.font.init()
        try:
            font = pygame.font.Font('resources'+os.sep+'DejaVuSansCondensed-Bold.ttf', 18)
        except IOError:
            font = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.init()
        pygame.display.set_mode((0,0), pyg.HWSURFACE|pyg.DOUBLEBUF|pyg.FULLSCREEN)
        scrdim = pygame.display.get_surface().get_size()
        pygame.display.set_caption('page player')
        self.scroller = smart_scroller.SmartScroller()
        self.renderer = Renderer(pygame.display.get_surface(), font)
        self.renderer.scrdim = scrdim
        self.clock = pygame.time.Clock()

        self.comix = comix
        self.denoise_jpeg = denoise_jpeg
        self.ignore_small_rows = ignore_small_rows
        self.comic_id = 0
        self.next_comic_id = 0
        self.state = "entering_page"
        self.load_page(0)
        self.running = True
        self.callback = callback

    def load_page(self, page_id):
        self.comic_id = page_id 
        name = self.comix.get_filename(page_id)
        fil = self.comix.get_file(page_id)
        fil_data = fil.read()
        
        pixbuf = image_tools.load_pixbuf_data(fil_data)
        image = image_tools.pixbuf_to_pil(pixbuf)

        screen_width, screen_height = self.renderer.scrdim

        zoom = '1:1'
        zoom = 'width'
        zoom = 'widen 5:4'

        width, height = image.size
        if 'widen 5:4' == zoom:
            # widen to occupy 5:4 ratio zone on screen
            scr_hei = screen_height
            width_5_4 = scr_hei * 5 / 4
            multiplier = 1.0*width_5_4 / width
            width2 = width_5_4
            height2 = int(math.floor(height * multiplier))
        elif 'width' == zoom:
            # Match screen size.
            width2 = screen_width
            height2 = int(math.floor(1.0 * height * width2 / width))
        else:
            # Keep image native resolution
            width2, height2 = width, height

        # Don't upscale.
        if width2 > width or height2 > height:
            width2, height2 = width, height
        elif width2 != width or height2 != height:
            image = image.resize((width2, height2), Image.ANTIALIAS)
            pixbuf = image_tools.pil_to_pixbuf(image)

        page = pygame.image.fromstring(image.tostring(), (width2, height2), "RGB")
        
        self.renderer.page = page
        self.renderer.zoom_cache = {}
        
        self.scroller.setup_image(pixbuf)

        self.renderer.set_background_color(self.scroller._bg)

        if False:
            rows = []
            for f in self.scroller._frames:
                pos = (row.rect.x,
                       row.rect.y,
                       row.rect.x + row.rect.w - 1,
                       row.rect.y + row.rect.h - 1)
                rows.append(pos)
        else:
            rows = []
            fn = 0
            while fn < len(self.scroller._frames):
                f = self.scroller._frames[fn]
                w = max(f.rect.w, screen_width)
                h = max(f.rect.h, screen_height)
                self.scroller._view_x = 0
                self.scroller._view_y = 0
                self.scroller._view_width = w
                self.scroller._view_height = h
                pos = self.scroller.scroll(to_frame=fn)
                x, y, w, h = pos
                rows.append((x, y, x + w - 1, y + h - 1))
                if w > screen_width or \
                   h > screen_height:
                    fn += 1
                else:
                    fn = self.scroller._current_frames[1] + 1

        
        self.rows = rows
        self.row_id = 0
        self.progress = 0.0
        self.pos = self.oid2pos(0)
        self.src_pos = self.oid2pos(0)
        
    def oid2pos(self, oid):
        return self.rows[oid]
        
        
    def zoom(self):
        self.src_pos = self.pos
        self.state = 'zooming'
        self.progress = 0.0
        
    def unzoom(self):
        self.src_pos = self.pos
        self.state = 'change_row'
        self.progress = 0.0
       
    def flip_page(self, delta, rowwise = False):
        nci = self.comic_id
        nci += delta
        if nci<0:
            nci = 0
        if nci>=len(self.comix):
            nci = len(self.comix)-1
        if nci!=self.comic_id:
            self.next_comic_id = nci
            self.flip_dir = nci>self.comic_id
            self.flip_to_last = rowwise
            self.src_pos = self.pos
            self.state = "leaving_page"

    def navigate_row(self, delta, force=False):
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
            self.renderer.brightness = 255
            self.src_pos = self.pos
            self.state = "change_row"

    def shifted_page(self, forward = False):
        x0,y0,x1,y1 = self.pos
        w,h = self.renderer.scrdim
        ch = self.renderer.page.get_height()
        
        if forward: 
            shift=-h
        else:
            shift = ch
        return (x0,y0+shift,x1,y1+shift)

    def adjust_brightness(self, back = False):
            self.renderer.brightness = 55+int(200*self.progress)
            if not back:
                self.renderer.brightness = 255 - self.renderer.brightness
                
    def start_load_page(self):
        self.load_page(self.next_comic_id)
        if not self.flip_dir and self.flip_to_last:
            self.row_id = len(self.rows)-1
        else:
            self.row_id = 0
        self.target_pos = self.oid2pos(self.row_id)
        self.pos = self.target_pos
        self.src_pos = self.shifted_page(self.flip_dir)
        self.pos = self.src_pos

    def end_changing_page(self):
        self.renderer.brightness = 255
        self.renderer.render(self.pos)

    def add_msg(self, text, color=(128,255,160), ttl=1.5):
        image_f = self.renderer.font.render(text, True, color)
        image_b = self.renderer.font.render(text, True, (0,32,0))
        base = pygame.Surface((image_f.get_width()+3, image_f.get_height()+3), 0, 32)
        base.blit(image_b, (2,2))
        base.blit(image_f, (0,0))
        image = base
        image.set_colorkey((0,0,0))
        self.renderer.textimages.append([image,255,ttl])
        
    def show_help(self):
        self.state = 'help'
        self.renderer.show_help()
        

    states = {
        "change_row": {
            "motion": True,
            "target": lambda self: self.oid2pos(self.row_id),
            "changeto": "static"
        },
        "zooming": {
            "motion": True,
            "target": lambda self: (0, 0, self.renderer.page.get_width(), self.renderer.page.get_height()),
            "changeto": "zoomed"
        },
        "leaving_page": {
            "motion": True,
            "target": lambda self: self.shifted_page(not self.flip_dir),
            "changeto": "entering_page",
            "onfinish": start_load_page,
            #~ "onprogress": lambda self:self.adjust_brightness()
        },
        "entering_page": {
            "motion": True,
            "target": lambda self: self.oid2pos(self.row_id),
            "changeto": "static",
            #~ "onfinish": end_changing_page,
            #~ "onprogress": lambda self:self.adjust_brightness(True)
        },
        "static": {
            "motion": False
        },
        "zoomed": {
            "motion": False
        },
        "help": {
            "motion": False
        }
    }
    
    def quit(self):
        self.running = False
        return        
        
    def show_mode(self):
        pass
        # TODO: remove
    
    def process_event(self, event):
        if event.type == pyg.QUIT:
            self.quit()
        elif event.type == pyg.VIDEOEXPOSE:
            self.force_redraw = True
        elif event.type == pyg.KEYDOWN:
            if self.state == 'help':
                if event.key == pyg.K_ESCAPE or event.key == pyg.K_q:
                    self.state = 'change_row'
                    self.progress = 1
                return
            elif event.key == pyg.K_ESCAPE or event.key == pyg.K_q:
                self.quit()
            if event.key == pyg.K_RETURN:
                if self.state == 'zooming' or self.state == 'zoomed':
                    self.unzoom()
                else:
                    self.zoom()
            if event.key == pyg.K_F1:
                self.show_help()
                self.force_redraw = False
            if self.state not in ['leaving_page']:
                if event.key == pyg.K_LEFT:
                    if event.mod & pyg.KMOD_SHIFT:
                        self.flip_page(-5)
                    elif event.mod & pyg.KMOD_CTRL:
                        self.flip_page(-20)
                    else:
                        self.flip_page(-1)
                elif event.key == pyg.K_RIGHT:
                    if event.mod & pyg.KMOD_SHIFT:
                        self.flip_page(+5)
                    elif event.mod & pyg.KMOD_CTRL:
                        self.flip_page(+20)
                    else:
                        self.flip_page(+1)
                elif event.key == pyg.K_UP or event.key == pyg.K_BACKSPACE:
                    self.navigate_row(-1)
                elif event.key == pyg.K_DOWN or event.key == pyg.K_SPACE:
                    self.navigate_row(+1)

    def update_screen(self, msec):
        if self.state=='help':
            return
        if self.states[self.state]["motion"] or self.force_redraw or len(self.renderer.textimages)>0:
            if self.states[self.state]["motion"]:
                self.progress += 0.0035*msec
                
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
                else:
                    if "onprogress" in self.states[self.state]:
                        self.states[self.state]["onprogress"](self)
                    pos = [0]*4
                    p2 = (1-math.cos(math.pi*self.progress))/2
                    for i in xrange(4):
                        pos[i] = int(self.src_pos[i]*(1.0-p2) + target_pos[i]*p2)
                    self.pos = pos
            for ti in self.renderer.textimages:
                ti[2] -= msec/1000.0
                if ti[2]<0:
                    ti[1] = 255+255*2*ti[2]
            self.renderer.textimages = [ti for ti in self.renderer.textimages if ti[1]>0]
            
            self.renderer.render(self.pos, self.states[self.state]["motion"])
    
    def loop(self, events): 
        msec = self.clock.tick(50)
        self.force_redraw = False
        for event in events:
            self.process_event(event)
        self.update_screen(msec)
            
            
    def run(self):
        while self.running: 
            self.loop(pygame.event.get())
        pygame.quit()
        if self.callback!=None:
            self.callback()
        
if __name__=="__main__":
    try:
        import debug_scripts
    except ImportError:
        debug_scripts = False
    if debug_scripts:
        debug_scripts.go()


