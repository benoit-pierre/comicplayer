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
from array import array
import math

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
