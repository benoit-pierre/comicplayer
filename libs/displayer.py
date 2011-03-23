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

import pygame
import pygame.key
import math
import time
import subprocess
import StringIO

import pygame.locals as pyg

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
        pygame.display.set_mode((0,0), pyg.HWSURFACE|pyg.DOUBLEBUF|pyg.FULLSCREEN)
        scrdim = pygame.display.get_surface().get_size()
        pygame.display.set_caption('page player')
        self.renderer = Renderer(pygame.display.get_surface(), pygame.font.Font('freesansbold.ttf', 16))
        self.renderer.scrdim = scrdim
        self.clock = pygame.time.Clock()

        self.comix = comix
        self.comic_id = 0
        self.next_comic_id = 0
        self.state_rownav = False
        self.state = "entering_page"
        self.load_page(0)
        self.running = True
        self.callback = callback

    def load_page(self, page_id):
        self.comic_id = page_id 
        name = self.comix.get_filename(page_id)
        fil = self.comix.get_file(page_id)
        
        # widen to occupy 5:4 ratio zone on screen
        scr_hei = self.renderer.scrdim[1]
        width_5_4 = scr_hei * 5 / 4
        buf_size = 64 * 1024
        
        gm_cmdline = "gm convert - -enhance -normalize -filter Lanczos -resize %sx10000 -quality 0 BMP:-" % width_5_4
        
        gm_proc = subprocess.Popen(gm_cmdline, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        outdata, errdata = gm_proc.communicate(fil.read())
        
        page = pygame.image.load(StringIO.StringIO(outdata), "temp.bmp").convert(32)
        
        self.renderer.page = page
        self.renderer.zoom_cache = {}
        
        hei = 1.0 * page.get_height()
        
        offsets = []
        extra_hei = hei - self.renderer.scrdim[1]
        scrolls = int(math.ceil(extra_hei/self.renderer.scrdim[1]*2))
        for i in range(scrolls+1):
            offsets.append(int(round(i*extra_hei/scrolls)))
        
        self.offsets = offsets
        self.offset_id = 0
        self.progress = 0.0
        self.pos = self.oid2pos(0)
        self.src_pos = self.oid2pos(0)
        self.add_msg(self.comix.get_filename(page_id))
        
    def oid2pos(self, oid):
        offset = self.offsets[oid]
        shei = self.renderer.scrdim[1]
        pwid = self.renderer.page.get_width()
        return [0, offset, pwid, offset+shei]
        
        
    def zoom(self):
        self.src_pos = self.pos
        self.state = 'zooming'
        self.progress = 0.0
        
    def unzoom(self):
        self.src_pos = self.pos
        self.state = 'change_offset'
        self.progress = 0.0
       
    def flip_page(self, delta, offsetwise = False):
        nci = self.comic_id
        nci += delta
        if nci<0:
            nci = 0
        if nci>=len(self.comix):
            nci = len(self.comix)-1
        if nci!=self.comic_id:
            self.next_comic_id = nci
            self.flip_dir = nci>self.comic_id
            self.flip_to_last = offsetwise
            self.src_pos = self.pos
            self.state = "leaving_page"

    def navigate_offset(self, delta, force=False):
        oid = self.offset_id
        oid += delta
        if oid<0:
            self.flip_page(-1,True)
            return
        if oid>=len(self.offsets):
            self.flip_page(+1)
            return
        if force or self.offset_id!=oid:
            self.offset_id = oid
            self.progress = 0.0
            self.renderer.brightness = 255
            self.src_pos = self.pos
            self.state = "change_offset"

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
        print self.flip_dir
        if not self.flip_dir and self.flip_to_last:
            self.offset_id = len(self.offsets)-1
        else:
            self.offset_id = 0
        self.target_pos = self.oid2pos(self.offset_id)
        self.pos = self.target_pos
        self.src_pos = self.shifted_page(self.flip_dir)
        self.pos = self.src_pos

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
        "change_offset": {
            "motion": True,
            "target": lambda self: self.oid2pos(self.offset_id),
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
            "target": lambda self: self.oid2pos(self.offset_id),
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
        self.add_msg("QUITTING...", color=(255,64,80), ttl=4)
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
                    self.state = 'change_offset'
                    self.progress = 1
                return
            elif event.key == pyg.K_ESCAPE or event.key == pyg.K_q:
                self.quit()
            if self.state == 'zooming' or self.state == 'zoomed':
                self.unzoom()
            else:
                if event.key == pyg.K_RETURN:
                    self.zoom()
                if event.key == pyg.K_F1:
                    self.show_help()
                    self.force_redraw = False
                if event.key == pyg.K_r:
                    self.state_rownav = not self.state_rownav
                    self.show_mode()
                    self.navigate_offset(0, True)
                if self.state not in ['zoomed', 'leaving_page']:
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
                    elif event.key == pyg.K_UP:
                        self.navigate_offset(-1)
                    elif event.key == pyg.K_DOWN or event.key == pyg.K_SPACE:
                        self.navigate_offset(+1)

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
