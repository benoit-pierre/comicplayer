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
import math

from displayer_help import help


class Renderer:
    
    def __init__(self, screen, font):
        self.fade = 6
        self.zoom_cache = {}
        self.brightness = 255
        self.screen = screen
        self.font = font
        self.scrdim = self.screen.get_width(), self.screen.get_height()
        self.textimages = []
        
    def zoomed_comic(self, spotlight, fast=False):
        pageW, pageH = self.page.get_width(), self.page.get_height()
        centerX, centerY = (spotlight[2]+spotlight[0])/2, (spotlight[3]+spotlight[1])/2
        spotW, spotH = spotlight[2]-spotlight[0], spotlight[3]-spotlight[1]
        spotAR = 1.0*spotW/spotH
        screenAR = 1.0*self.scrdim[0]/self.scrdim[1]
        
        if screenAR>spotAR:
            spotW = int(round(spotH*screenAR))
        else:
            spotH = int(round(spotW/screenAR))
            
        # comic-to-screen conversion is: scrX = a*comX  + bX , scrY = a*comY  + bY
        
        a = 1.0*self.scrdim[1]/spotH
        bX = (self.scrdim[0]//2) - int(round(a*centerX))
        bY = (self.scrdim[1]//2) - int(round(a*centerY))
            
        wx, wy = centerX-spotW/2, centerY-spotH/2
        wxe, wye = centerX+spotW/2, centerY+spotH/2
        

        if wx<0: 
            wx = 0
        if wxe>=pageW: wxe = pageW-1
        if wy<0: 
            wy = 0
        if wye>=pageH: wye = pageH-1
     
        shift = (a*wx+bX, a*wy+bY)
        
        ww, wh = wxe-wx, wye-wy
        rect = (wx, wy, ww, wh)
        dims = (int(round(ww*a)), int(round(wh*a)))
        
        
        if rect in self.zoom_cache:
            resized = self.zoom_cache[rect]
        else:
            if ww==pageW and wh==pageH:
                source = self.page
            else:
                source = self.page.subsurface(rect)
            if fast:
                resized = pygame.transform.scale(source, dims)
            else:
                resized = pygame.transform.smoothscale(source, dims)
                self.zoom_cache[rect] = resized
        return resized, shift

    def render(self, pos, motion=False):
        sw, sh = self.scrdim

        wid, hei = pos[2]-pos[0], pos[3]-pos[1]
        k = min(1.0*sw/wid, 1.0*sh/hei)
        if k<1:
            cw, ch = self.page.get_width(), self.page.get_height()
            if pos[0]>cw or pos[1]>ch or pos[2]<0 or pos[3]<0:
                page = None
            else:
                page, shift = self.zoomed_comic(pos, motion)
        else:
            page = self.page
            marg_x = (self.scrdim[0]-wid)//2
            marg_y = (self.scrdim[1]-hei)//2
            shift = marg_x-pos[0], marg_y-pos[1]
        self.screen.fill((0,0,0))
        if page!=None:
            self.screen.blit(page, shift)
        self.show_texts()
        pygame.display.flip()

    def zoom(self):
        page = self.page
        scrdim = self.scrdim
        cw, ch = page.get_width(), page.get_height()
        sw, sh = scrdim
        page, shift = self.zoomed_comic((0,0,cw,ch))
        wid, hei = page.get_width(), page.get_height()
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
