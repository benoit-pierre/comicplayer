# coding: UTF-8

#   Copyright (c) 2009-2010, Konstantin Yegupov
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

import pygame, sys,os
import pygame.key
import time, math
import copy
import glob

from array import array
from pygame.locals import * 

from comic_book import ComicBook
from displayer_help import help
from displayer_renderer import Renderer

def rect_center(r):
    return [(r[0]+r[2])/2, (r[1]+r[3])/2]

def xy_range(xy1, xy2):
    return (xy2[0]-xy1[0])**2 + (xy2[1]-xy1[1])**2

def xy_rhombic_range(xy1, xy2):
    return abs(xy2[0]-xy1[0]) + abs(xy2[1]-xy1[1])


class DisplayerApp:
    def __init__(self, comix, callback=None):
        pygame.init()
        window = pygame.display.set_mode((0,0), HWSURFACE|DOUBLEBUF|FULLSCREEN)
        scrdim = pygame.display.get_surface().get_size()
        pygame.display.set_caption('page player')
        self.renderer = Renderer(pygame.display.get_surface(), pygame.font.Font('freesansbold.ttf', 16))
        self.renderer.scrdim = scrdim
        self.clock = pygame.time.Clock()

        self.comix = comix
        self.comic_id = 0
        self.next_comic_id = 0
        self.state_spotlight = True
        self.state_rownav = False
        self.state = "entering_page"
        self.load_page(0)
        self.running = True
        self.callback = callback

    def load_page(self, page_id):
        self.comic_id = page_id 
        name = self.comix.get_filename(page_id)
        fil = self.comix.get_file(page_id)
        page = pygame.image.load(fil, name).convert(32)
        self.renderer.page = page
        self.renderer.zoom_cache = {}
        
        #~ panels = self.comix.load_panels(page_id)
        hei = 1.0 * page.get_height()
        scrolls = math.floor(hei/self.renderer.scrdim[1]*2)
        
        panels = []
        for i in range(scrolls):
            panels.append((0, int(round(i*hei/scrolls)), page.get_width()-1, int(round((i+1)*hei/scrolls))))
        
        self.raw_panels = panels
        self.panel_id = 0
        self.load_nav(self.state_rownav)
        self.progress = 0.0
        self.pos = copy.copy(panels[self.panel_id])
        self.src_pos = self.pos
        self.add_msg(self.comix.get_filename(page_id))
        
    def load_nav(self, rownav = False, convert_id = True):
        panels = self.raw_panels
        oldid = self.panel_id
        if rownav or convert_id:
            rows = []
            y0 = -1
            for i, p in enumerate(panels):
                if p[1] == y0 and p[3]==y1: 
                    x1 = p[2]
                else:
                    if y0>=0:
                        rows.append([x0, y0, x1, y1])
                    x0, y0, x1, y1 = p
                    if convert_id and not rownav and len(rows)==oldid:
                        self.panel_id = i
                if convert_id and rownav and i==oldid:
                    self.panel_id = len(rows)
            rows.append([x0, y0, x1, y1])
        if rownav:
            self.panels = rows
        else:
            self.panels = panels
    
    def zoom(self):
        self.src_pos = self.pos
        self.state = 'zooming'
        self.progress = 0.0
        
    def unzoom(self):
        self.src_pos = self.pos
        self.state = 'change_panel'
        self.progress = 0.0
       
    def flip_page(self, delta, panelwise = False):
        nci = self.comic_id
        nci += delta
        if nci<0:
            nci = 0
        if nci>=len(self.comix):
            nci = len(self.comix)-1
        if nci!=self.comic_id:
            self.next_comic_id = nci
            self.flip_dir = nci>self.comic_id
            self.flip_to_last = panelwise
            self.src_pos = self.pos
            self.state = "leaving_page"

    def navigate_panel(self, delta, force=False):
        pid = self.panel_id
        pid += delta
        if pid<0:
            self.flip_page(-1,True)
            return
        if pid>=len(self.panels):
            self.flip_page(+1)
            return
        if force or self.panel_id!=pid:
            self.panel_id = pid
            self.progress = 0.0
            self.renderer.brightness = 255
            self.src_pos = self.pos
            self.state = "change_panel"

    def navigate_horizontal(self, delta):
        if delta==0:
            return
        pid = self.panel_id
        p0 = self.panels[pid]
        if delta>0:
            filt = lambda p0, p: p[0]>p0[0] and not(p[3]<=p0[1] or p[1]>=p0[3])
        else:
            filt = lambda p0, p: p[0]<p0[0] and not(p[3]<=p0[1] or p[1]>=p0[3])
        
        candidates = [pid_rect for pid_rect in enumerate(self.panels) if filt(p0, pid_rect[1])]
            
        c0 = rect_center(p0)
        def centerrange(pid_rect):
            return xy_rhombic_range(rect_center(pid_rect[1]), c0)
        candidates.sort(key=centerrange)
        
        if len(candidates)==0:
            self.navigate_panel(delta)
            return
        else:
            self.panel_id = candidates[0][0]
            self.progress = 0.0
            self.renderer.brightness = 255
            self.src_pos = self.pos
            self.state = "change_panel"


    def navigate_vertical(self, delta):
        if delta==0:
            return
        pid = self.panel_id
        p0 = self.panels[pid]
        if delta>0:
            filt = lambda p0, p: p[1]>p0[1] and not(p[2]<=p0[0] or p[0]>=p0[2])
        else:
            filt = lambda p0, p: p[1]<p0[1] and not(p[2]<=p0[0] or p[0]>=p0[2])
        
        candidates = [pid_rect for pid_rect in enumerate(self.panels) if filt(p0, pid_rect[1])]
            
        c0 = rect_center(p0)
        def centerrange(pid_rect):
            return xy_rhombic_range(rect_center(pid_rect[1]), c0)
        candidates.sort(key=centerrange)
        
        if len(candidates)==0:
            self.flip_page(delta,delta<0)
            return
        else:
            self.panel_id = candidates[0][0]
            self.progress = 0.0
            self.renderer.brightness = 255
            self.src_pos = self.pos
            self.state = "change_panel"

    def shifted_page(self, back = False):
        x0,y0,x1,y1 = self.pos
        w,h = self.renderer.scrdim
        cw = self.renderer.page.get_width()
        
        if back: 
            shift=-x1
        else:
            shift = cw-x0
        return (x0+shift,y0,x1+shift,y1)

    def adjust_brightness(self, back = False):
            self.renderer.brightness = 55+int(200*self.progress)
            if not back:
                self.renderer.brightness = 255 - self.renderer.brightness
                
    def start_load_page(self):
        self.load_page(self.next_comic_id)
        if not self.flip_dir and self.flip_to_last:
            self.panel_id = len(self.panels)-1
        else:
            self.panel_id = 0
        self.target_pos = self.panels[self.panel_id]
        self.pos = self.target_pos
        self.src_pos= self.shifted_page(self.flip_dir)

    def end_changing_page(self):
        self.renderer.brightness = 255
        self.renderer.render(self.pos)

    def add_msg(self, text, color=(128,255,160), ttl=1.5):
        image_f = self.renderer.font.render(text, True, color)
        image_b = self.renderer.font.render(text, True, (0,32,0))
        base = pygame.Surface((image_f.get_width()+2, image_f.get_height()+2), 0, 32)
        base.blit(image_b, (2,2))
        base.blit(image_f, (0,0))
        image = base.convert(8)
        image.set_colorkey((0,0,0))
        self.renderer.textimages.append([image,255,ttl])
        
    def show_help(self):
        self.state = 'help'
        self.renderer.show_help()
        

    states = {
        "change_panel": {
            "motion": True,
            "target": lambda self: self.panels[self.panel_id],
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
            "nospotlight": True,
            #~ "onprogress": lambda self:self.adjust_brightness()
        },
        "entering_page": {
            "motion": True,
            "target": lambda self: self.panels[self.panel_id],
            "changeto": "static",
            #~ "onfinish": end_changing_page,
            "nospotlight": True,
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
        mode = "cell"
        if self.state_rownav:
            mode = "row"
        if self.state_spotlight:
            mode += " spotlight"
        else:
            mode += " focus"
        self.add_msg("Highlight mode: " + mode)
    
    def process_event(self, event):
        if event.type == QUIT:
            self.quit()
        elif event.type == VIDEOEXPOSE:
            self.force_redraw = True
        elif event.type == KEYDOWN:
            if self.state == 'help':
                if event.key == K_ESCAPE or event.key == K_q:
                    self.state = 'change_panel'
                    self.progress = 1
                return
            elif event.key == K_ESCAPE or event.key == K_q:
                self.quit()
            if self.state == 'zooming' or self.state == 'zoomed':
                self.unzoom()
            else:
                if event.key == K_SPACE:
                    self.zoom()
                if event.key == K_h:
                    self.state_spotlight = not self.state_spotlight
                    self.show_mode()
                    self.force_redraw = True
                if event.key == K_F1:
                    self.show_help()
                    self.force_redraw = False
                if event.key == K_r:
                    self.state_rownav = not self.state_rownav
                    self.show_mode()
                    self.load_nav(self.state_rownav, True)
                    self.navigate_panel(0, True)
                if self.state not in ['zoomed', 'leaving_page']:
                    if event.key == K_PAGEUP:
                        if event.mod & KMOD_SHIFT:
                            self.flip_page(-5)
                        elif event.mod & KMOD_CTRL:
                            self.flip_page(-20)
                        else:
                            self.flip_page(-1)
                    elif event.key == K_PAGEDOWN:
                        if event.mod & KMOD_SHIFT:
                            self.flip_page(+5)
                        elif event.mod & KMOD_CTRL:
                            self.flip_page(+20)
                        else:
                            self.flip_page(+1)
                    elif event.key == K_LEFT:
                        self.navigate_panel(-1)
                    elif event.key == K_RIGHT:
                        self.navigate_panel(+1)
                    elif event.key == K_UP:
                        self.navigate_vertical(-1)
                    elif event.key == K_DOWN:
                        self.navigate_vertical(+1)

    def update_screen(self, msec):
        if self.state=='help':
            return
        if self.states[self.state]["motion"] or self.force_redraw or len(self.renderer.textimages)>0:
            light = "spot" if self.state_spotlight else "bright"
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
            
            self.renderer.render(self.pos, self.states[self.state]["motion"], light)
    
    def loop(self, events): 
        msec = self.clock.tick(50)
        self.force_redraw = False
        for event in events:
            self.process_event(event)
        self.update_screen(msec)
            
            
    def run(self):
        self.add_msg("Press F1 for help", color=(255,64,80), ttl=4)
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
