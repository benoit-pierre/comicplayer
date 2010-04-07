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

def rect_center(r):
    return [(r[0]+r[2])/2, (r[1]+r[3])/2]

def xy_range(xy1, xy2):
    return (xy2[0]-xy1[0])**2 + (xy2[1]-xy1[1])**2

def xy_rhombic_range(xy1, xy2):
    return abs(xy2[0]-xy1[0]) + abs(xy2[1]-xy1[1])


class Renderer:
    
    def __init__(self, screen, font):
        self.fade = 6
        c_precalc = []
        for i in xrange(self.fade+1):
            c_precalc.append(array("f"))
            for j in xrange(self.fade+1):
                a = 1-0.16*(math.sqrt(i*i+j*j))
                if a<0:
                    a = 0
                c_precalc[-1].append(a)
        self.c_precalc = c_precalc
        self.zoom_cache = {}
        self.brightness = 255
        self.screen = screen
        self.font = font
        self.scrdim = self.screen.get_width(), self.screen.get_height()
        self.textimages = []
        
    def zoomed_comic(self, pos, fast=False):
        cw, ch = self.page.get_width(), self.page.get_height()
        pw, ph = pos[2]-pos[0], pos[3]-pos[1]
        sw, sh = self.scrdim
        kx, ky = 1.0*sw/pw, 1.0*sh/ph
        k = min(kx, ky)
        # TODO: продумать все округления
        pw2, ph2 = (int(round(pw*k)), int(round(ph*k))) # новый размер спотлайта
        mx, my = (sw-pw2)//2, (sh-ph2)//2 # смещение спотлайта на экране
        mx2, my2 = (int(round(mx/k)), int(round(my/k))) # смещение спотлайта на экране в старых единицах
        
        wx, wy = pos[0]-mx2, pos[1]-my2 # начало окна в старом комиксе
        wxe, wye = wx+pw+2*mx2, wy+ph+2*my2 # конец окна в старом комиксе

        if wx<0: wx = 0
        if wxe>=cw: wxe = cw-1
        if wy<0: wy = 0
        if wye>=ch: wye = ch-1
        ww, wh = wxe-wx, wye-wy
        rect = (wx, wy, ww, wh)
        dims = (int(round(ww*k)), int(round(wh*k)))
        pos1x, pos1y = pos[0]-wx, pos[1]-wy # начало спотлайта в вырезке
        pos2x, pos2y = (int(round(pos1x*k)), int(round(pos1y*k))) # начало спотлайта в ресайзеной вырезке
        
        if (rect, False) in self.zoom_cache:
            resized = self.zoom_cache[(rect, False)]
        elif (rect, fast) in self.zoom_cache:
            resized = self.zoom_cache[(rect, fast)]
        else:
            if ww==cw and wh==ch:
                source = self.page
            else:
                source = self.page.subsurface(rect)
            if fast:
                resized = pygame.transform.scale(source, dims)
            else:
                self.zoom_cache[(rect, False)] = pygame.transform.smoothscale(source, dims)
                resized = self.zoom_cache[(rect, fast)]
        return resized, (pos2x, pos2y), (pw2, ph2)

    @staticmethod
    def pixblend(src, dest, todo):
        for x0, y0, x1, y1, a in todo:
            p1 = src[x0][y0]
            p2 = dest[x1][y1]
            b1 = p1 & 255
            b2 = p2 & 255
            g1 = (p1>>8) & 255
            g2 = (p2>>8) & 255
            r1 = (p1>>16) & 255
            r2 = (p2>>16) & 255
            b = (b1*a + b2*(255-a))//255
            g = (g1*a + g2*(255-a))//255
            r = (r1*a + r2*(255-a))//255
            dest[x1][y1] = (((r<<8)+g)<<8)+b
    
    def fuzz_blit(self, dest, src, dest_coord, src_rect):
        x0, y0, w, h = src_rect
        dx0, dy0 = dest_coord
        fade = self.fade
        x0+=fade//2;    y0+= fade//2;
        w-= 2*fade//2;    h-= 2*fade//2
        dx0+= fade//2;    dy0+= fade//2
        src.set_alpha(self.brightness)
        dest.blit(src, (dx0,dy0), (x0,y0,w,h))
        cw, ch = src.get_width(), src.get_height()
        if x0>=cw or y0>=ch or x0+w<0 or y0+h<0:
            return
       
        x1 = x0 + w - 1
        y1 = y0 + h - 1
        dx1 = dx0 + w - 1
        dy1 = dy0 + h - 1
        c_precalc = self.c_precalc
        for i in xrange(1,fade+1):
            src.set_alpha(int(self.brightness*c_precalc[0][i]))
            dest.blit(src, (dx0, dy0-i), (x0, y0-i, w, 1))
            dest.blit(src, (dx0, dy1+i), (x0, y1+i, w, 1))
            dest.blit(src, (dx0-i, dy0), (x0-i, y0, 1, h))
            dest.blit(src, (dx1+i, dy0), (x1+i, y0, 1, h))
        sw, sh = self.scrdim
        
        pxa_src = pygame.PixelArray(src)
        pxa_dest = pygame.PixelArray(self.screen)
        lim_i0 = min(x0, dx0)
        lim_i1 = min(cw-1-x1, sw-1-dx1)
        lim_j0 = min(y0, dy0)
        lim_j1 = min(ch-1-y1, sh-1-dy1)
        todo = []
        for i in xrange(1, fade+1):
            for j in xrange(1, fade+1):
                a = int(self.brightness*c_precalc[i][j])
                if a==0:
                    continue
                if i<lim_i0 and j<lim_j0:
                    todo.append((x0-i, y0-j, dx0-i, dy0-j, a))
                if i<lim_i1 and j<lim_j0:
                    todo.append((x1+i, y0-j, dx1+i, dy0-j,a))
                if i<lim_i0 and j<lim_j1:
                    todo.append((x0-i, y1+j, dx0-i, dy1+j, a))
                if i<lim_i1 and j<lim_j1:
                    todo.append((x1+i, y1+j, dx1+i, dy1+j, a))
        self.pixblend(pxa_src, pxa_dest, todo)
        del pxa_src
        del pxa_dest

    
    def render(self, pos, motion=False, mode="spot"):
        wid, hei = pos[2]-pos[0], pos[3]-pos[1]
        sw, sh = self.scrdim
        k = min(1.0*sw/wid, 1.0*sh/hei)
        if k<1:
            cw, ch = self.page.get_width(), self.page.get_height()
            if pos[0]>cw or pos[1]>ch or pos[2]<0 or pos[3]<0:
                page = None
            else:
                page, start, size = self.zoomed_comic(pos, motion)
                x0, y0 = start
                wid, hei = size
        else:
            page = self.page
            x0, y0 = pos[0], pos[1]
        self.screen.fill((0,0,0))
        if page!=None:
            marg_x = (self.scrdim[0]-wid)//2
            marg_y = (self.scrdim[1]-hei)//2
            q = 1.0 if mode=="bright" else 0.4
            page.set_alpha(int(self.brightness*q))
            self.screen.blit(page, (marg_x-x0, marg_y-y0))
            if mode=="spot":
                self.fuzz_blit(self.screen, page, (marg_x, marg_y), (x0, y0, wid, hei))
        self.show_texts()
        pygame.display.flip()

    def zoom(self):
        page = self.page
        scrdim = self.scrdim
        cw, ch = page.get_width(), page.get_height()
        sw, sh = scrdim
        k = min(1.0*sw/cw, 1.0*sh/ch)
        page, start, size = self.zoomed_comic((0,0,cw,ch))
        wid, hei = size
        marg_x = (scrdim[0]-wid)//2
        marg_y = (scrdim[1]-hei)//2
        page.set_alpha(255)
        self.screen.fill((0,0,0))
        self.screen.blit(page, (marg_x, marg_y))
        self.show_texts()
        pygame.display.flip()

    def center(rect):
        return [(rect[0]+rect[2])//2, (rect[1]+rect[3])//2]

    def range2d(x, y):
        return math.sqrt((y[0]-x[0])**2 + (y[1]-x[1])**2)
    
    def show_texts(self):
        bottom = self.scrdim[1]
        for ti in reversed(self.textimages):
            image, alpha, ttl = ti
            image.set_alpha(alpha)
            rect = image.get_rect()
            rect.left = 0
            rect.bottom = bottom
            bottom -= 16
            self.screen.blit(image, rect)
        
    def write(self, text, x, y):
        image = self.font.render(text, True, (160,255,128))
        rect = image.get_rect()
        self.screen.blit(image, (x,y))
        
    def show_help(self):
        self.screen.fill((0,0,0))
        top = 20
        for line in help.splitlines():
            keys, desc = line.strip().split(':',1)
            self.write(keys, self.scrdim[0]/4, top)
            self.write(desc, self.scrdim[0]/2, top)
            top += 20
        pygame.display.flip()
        

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
        panels = self.comix.load_panels(page_id)
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
            print self.state, event.key
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
