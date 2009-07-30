#   Copyright (c) 2009, Konstantin Yegupov
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

from fltk import *
import sys

import Image

from comic_book import ComicBook
from auto_segment import segmentate, seg_algos

import traceback

def fill_rect(x0, y0, w, h):
    step = 5
    for x in range(x0, x0+w, step):
        leng = min(h, x0+w-x)-1
        fl_line(x, y0, x+leng, y0+leng)
    for y in range(y0+step, y0+h, step):
        leng = min(w, y0+h-y)-1
        fl_line(x0, y, x0+leng, y+leng)

class BaseEditor:
    def __init__(self, widget):
        self.widget = widget
        self.pulling = None
        self.pullstart = None
        self.app = self.widget.app

class GridEditor(BaseEditor):
    def __init__(self, widget):
        BaseEditor.__init__(self, widget)
    
    def draw(self):
        print 'y'
        x0,y0 = -self.widget.x(), -self.widget.y()
        w,h = self.widget.w(), self.widget.h()
        app = self.widget.app
        fl_color(255, 192, 192)
        hls = app.hlines
        vls = app.vlines
        zq = self.widget.zoom_q
        for y in hls:
            fl_line(-x0,y/zq-y0,w-x0,y/zq-y0)
        for x in vls:
            fl_line(x/zq-x0,-y0,x/zq-x0,h-y0)
        fl_color(255, 0, 0)
        for i,r in enumerate(app.rects):
            xr0, yr0, xr1, yr1 = r[0]/zq, r[1]/zq, r[2]/zq, r[3]/zq
            fl_rect(xr0-x0, yr0-y0, xr1-xr0+1, yr1-yr0+1)
            if i == self.widget.app.selected_panel:
                fill_rect(xr0-x0, yr0-y0, xr1-xr0+1, yr1-yr0+1)

    def get_snap(self, x, y):
        app = self.widget.app
        if app.mode=="p":
            ar = app.rects
            for i, r in enumerate(ar):
                x0,y0,x1,y1 = r
                if x0<=x<=x1 and y0<=y<=y1:
                    return i
            return None
        if app.mode=="h":
            lines = app.hlines
            point = y
        elif app.mode=="v":
            lines = app.vlines
            point = x
    
        for i,l in enumerate(lines):
            if abs(point-l)<8:
                return i
        return None

    def start_drag(self, x, y):
        app = self.app
        i = self.get_snap(x, y)
        if i>-1:
            self.pulling = i
            self.pullstart = (x,y)
            return True
        return False

    def do_drag(self, x, y):
        app = self.app
        if self.pulling!=None:
            if app.mode == "h":
                app.update_rects(self.pulling, y, app.mode)
                app.hlines[self.pulling] = y
            if app.mode == "v":
                app.update_rects(self.pulling, x, app.mode)
                app.vlines[self.pulling] = x
            if app.mode == "p":
                cell0 = app.get_cell(self.pullstart)
                cell1 = app.get_cell((x,y))
                if cell1!=None:
                    app.rects[self.pulling] = app.from_cell_to_cell(cell0, cell1)
                    app.remove_duplicate_rects()
            app.refresh_text()
            self.widget.damage(1)

    def end_drag(self):
        app = self.app
        if self.pulling:
            app.refresh_text()
        self.pulling = None
        if app.mode!="p" and app.remerge_lines():
            self.widget.damage(1)

    def click(self, x, y):
        app = self.app
        if app.mode == "h":
            app.hlines.append(y)
            self.pulling = len(app.hlines)-1
        if app.mode == "v":
            app.vlines.append(x)
            self.pulling = len(app.vlines)-1
        if app.mode == "p":
            cell = app.get_cell((x,y))
            if cell==None:
                return
            app.rects.append(app.from_cell_to_cell(cell, cell))
            self.pulling = len(app.rects)-1
            self.pullstart = (x,y)
        app.refresh_text()
        self.widget.damage(1)

    def rclick(self, x, y):
        app = self.app
        i = self.get_snap(x, y)
        if i>-1:
            if app.mode == "h":
                v = app.hlines[i]
                del app.hlines[i]
                app.rects = [r for r in app.rects if r[1]!=v and r[3]!=v]
            if app.mode == "v":
                v = app.vlines[i]
                del app.vlines[i]
                app.rects = [r for r in app.rects if r[0]!=v and r[2]!=v]
            if app.mode == "p":
                del app.rects[i]
            app.refresh_text()
            self.widget.damage(1)


class PanelEditor(BaseEditor):
    def __init__(self, widget):
        BaseEditor.__init__(self, widget)
    

class MyCanvas(Fl_Widget):
    def __init__(self, app, x, y, w, h, editorClass):
        Fl_Widget.__init__(self, x ,y, w, h)
        self.app = app
        self.cur = FL_CURSOR_DEFAULT
        self.editor = editorClass(self)
    
    def draw(self):
        print 'a'
        w,h = self.w(), self.h()
        iw,ih = self.im.size
        app = self.app
        x0,y0 = 10-self.x(), 10-self.y()
        
        x1 = min(iw, x0+w)
        y1 = min(ih, y0+h)
        ims = self.im.crop((x0, y0, x1, y1))
        fl_draw_image_mono(ims.tostring(), 10, 10, ims.size[0], ims.size[1]) 
        print 'x'
        
        try:
            self.editor.draw()
        except Exception, e:
            traceback.print_exc()
            raise
        


    def set_cur(self, cur):
        if self.cur!=cur:
            self.window().cursor(cur)
            self.cur = cur

       
    def handle(self, event):
        print '1'
        zq = self.zoom_q
        x0,y0 = self.x(), self.y()
        y = (Fl.event_y()-y0)
        x = (Fl.event_x()-x0)
        if x<0: x = 0
        if y<0: y = 0
        im = self.im
        if x>=im.size[0]: x = im.size[0]-1
        if y>=im.size[1]: y = im.size[1]-1
            
        x *= zq
        y *= zq
            
        app = self.app
        btn = Fl.event_button()
        print '2'
        try:
            if event == FL_PUSH:
                if btn==1:
                    if not self.editor.start_drag(x, y):
                        self.editor.click(x, y)
                if btn==3:
                    self.editor.rclick(x, y)
                return 1
            elif event == FL_DRAG:
                if btn==1:
                    self.editor.do_drag(x, y)
                return 1
            elif event == FL_RELEASE:
                if btn==1:
                    if self.editor.pulling!=None:
                        self.editor.end_drag()
                return 1
            elif event == FL_ENTER:
                i = self.editor.get_snap(x, y)
                self.set_cur(FL_CURSOR_HAND if i>-1 else FL_CURSOR_CROSS)
                return 1
            elif event == FL_MOVE:
                i = self.editor.get_snap(x, y)
                self.set_cur(FL_CURSOR_HAND if i>-1 else FL_CURSOR_CROSS)
                return 1
            elif event == FL_LEAVE:
                self.set_cur(FL_CURSOR_DEFAULT)
                return 1
            else:
                return Fl_Widget.handle(self, event)
        except Exception, e:
            traceback.print_exc()
            raise

class PanelList(Fl_Hold_Browser):
    def __init__(self, app, *vargs):
        self.dragged = None
        self.app = app
        Fl_Hold_Browser.__init__(self, *vargs)
    
    def handle(self, event):
        try:
            btn = Fl.event_button()
            res = Fl_Hold_Browser.handle(self, event)
            if event == FL_PUSH:
                if btn==1:
                    self.dragged = self.value()
            elif event == FL_DRAG:
                if btn==1:
                    frm = self.dragged
                    to = self.value()
                    if frm!=to:
                        if frm!=0 and to!=0:
                            rects = self.app.rects
                            tmp = rects[to-1]
                            rects[to-1] = rects[frm-1]
                            rects[frm-1] = tmp
                            tmp = self.text(to)
                            self.text(to, self.text(frm))
                            self.text(frm, tmp)
                            self.value(to)
                        self.dragged = to
            return res 
        except Exception, e:
            traceback.print_exc()
            return 0
        

class SegEditorApp:
    def open_file(self, widhet):
        self.pathbox.value(fl_file_chooser("Open Comic File", "JPEG Files (*.jpg)\tPNG Files (*.png)\tGIF Files (*.gif)\tAll Files (*)", None))
        
    def open_dir(self, widget):
        self.pathbox.value(fl_dir_chooser("Open Comic Folder", None))

    def update_rects(self, i, x1, mode):
        if self.mode=="h":
            lines = self.hlines
            inds = 1,3
        elif self.mode=="v":
            lines = self.vlines
            inds = 0,2
        x0 = lines[i]
        for r in self.rects:
            if r[inds[0]] == x0:
                r[inds[0]] = x1
            if r[inds[1]] == x0:
                r[inds[1]] = x1

    def remove_duplicate_rects(self):
        for i in range(len(self.rects)-1):
            for i2 in range(len(self.rects)-1, i, -1):
                r = self.rects[i]; r2 = self.rects[i2]
                if r==r2:
                    del self.rects[i2]
    
    def remerge_lines(self):
        changed = False
        if self.mode=="h":
            lines = self.hlines
            inds = 1,3
        elif self.mode=="v":
            lines = self.vlines
            inds = 0,2
        for i in range(len(lines)-1):
            for i2 in range(len(lines)-1, i, -1):
                l = lines[i]; l2 = lines[i2]
                if abs(l2-l)<8:
                    self.update_rects(i2, l, self.mode)
                    del lines[i2]
                    changed = True
        if changed:
            self.remove_duplicate_rects()
        return changed

    def set_edit_mode(self, widget):
        self.emode = widget.mode
        if widget.mode=='p':
            self.help.value("Drag panel corners to resize them.")
            self.rb_h.deactivate()
            self.rb_v.deactivate()
            self.rb_p.deactivate()
        else:
            self.rb_h.activate()
            self.rb_v.activate()
            self.rb_p.activate()
            self.set_grid_mode(self.rb_h)
        widget.setonly()

    def set_grid_mode(self, widget):
        self.mode = widget.mode
        if widget.mode in ["h", "v"]:
            self.help.value("Left button click - create line.\nLeft button drag - move line.\nRight button click - delete line.")
        else:
            self.help.value("Left button click - create panel.\nLeft button drag - modify panel.\nRight button click - delete panel.")
        widget.setonly()

    def get_cell(self, xy):
        hls = self.hlines
        vls = self.vlines
        lefts = [l for l in vls if l<=xy[0]]
        rights = [l for l in vls if l>=xy[0]]
        tops = [l for l in hls if l<=xy[1]]
        bottoms = [l for l in hls if l>=xy[1]]
        if len(lefts)==0 or len(rights)==0 or len(tops)==0 or len (bottoms)==0:
            return None
        return (max(lefts), max(tops), min(rights), (min(bottoms)))
        
    def from_cell_to_cell(self, c0, c1):
        r = []
        r.append(min(c0[0],c1[0]))
        r.append(min(c0[1],c1[1]))
        r.append(max(c0[2],c1[2]))
        r.append(max(c0[3],c1[3]))
        return r

    def refresh_text(self):
        self.text.clear()
        for r in self.rects:
            self.text.add("@t%04s,%04s,%04s,%04s" % tuple(r))


    def flip_back(self, widget):
        self.try_change_page(self.page_id-1)
            
    def flip_fwd(self, widget):
        self.try_change_page(self.page_id+1)

    def select_page(self, widget):
        self.try_change_page(int(widget.value()))

    def try_change_page(self, new_page_id):
        if new_page_id>=0 and new_page_id<len(self.comix):
            if self.page_id!=new_page_id:
                self.save_page()
                self.page_id = new_page_id
                self.load_segmentation()
                self.spin_page.value(new_page_id)

    def set_zoom(self, widget):
        self.canvas.zoom_q = self.zooms[widget.value()][0]
        self.init_canvas()

    def init_canvas(self):
        zoom_q = self.canvas.zoom_q
        sz = self.image.size
        self.canvas.im = self.image.convert('L').resize((sz[0]/zoom_q, sz[1]/zoom_q), Image.ANTIALIAS)
        self.canvas.size(self.canvas.im.size[0], self.canvas.im.size[1])
        self.scroll.position(0, 0)
        self.scroll.redraw()
        self.canvas.redraw()

    def rects2lines(self):
        rects = self.rects
        self.hlines = list(set([r[1] for r in rects]+[r[3] for r in rects]))
        self.vlines = list(set([r[0] for r in rects]+[r[2] for r in rects]))

    def load_segmentation(self):
        page_id = self.page_id
        name = self.comix.get_filename(page_id)
        fil = self.comix.get_file(page_id)
        self.image = Image.open(fil)
        if page_id in self.cur_data:
            self.rects = self.cur_data[page_id]
        else:
            self.rects = self.comix.load_panels(page_id)
        
        self.rects2lines()
        self.refresh_text()
        
        self.canvas.selected = None
        
        self.init_canvas()

    def save_page(self):
        self.cur_data[self.page_id] = self.rects

    def commit_changes(self):
        for k, v in self.cur_data.iteritems():
            self.comix.save_panels(k, v)

    def done(self, widget):
        self.save_page()
        self.commit_changes()
        self.window.hide()
        if self.callback!=None:
            self.callback()
        
    def revert_segment(self, w):
        self.rects = self.comix.load_panels(self.page_id)
        self.rects2lines()
        self.refresh_text()
        self.canvas.redraw()
        
    def clear_segment(self, w):
        self.rects = [(0, 0, self.image.size[0]-1, self.image.size[1]-1)]
        self.rects2lines()
        self.refresh_text()
        self.canvas.redraw()
        
    def auto_segment(self, w):
        self.seg_window = Fl_Window(500, 110)
        self.algo = Fl_Choice(250, 10, 200, 20, "Segmentation algorithm")
        for c in seg_algos:
            self.algo.add(c.__name__)
        self.algo.value(0)
        self.seg_black = Fl_Input(250, 30, 50, 20, "Force background")
        self.seg_tol = Fl_Input(250, 50, 100, 20, "Tolerance")
        self.seg_tol.value("35")
        self.seg_go = Fl_Button(170, 80, 70, 20, "GO")
        self.seg_go.callback(self.do_auto_seg)
        self.seg_cancel = Fl_Button(260, 80, 70, 20, "Cancel")
        self.seg_cancel.callback(self.auto_seg_end)
        self.seg_window.end()
        self.seg_window.set_modal()
        self.seg_window.show(["Automatic segmentation"])
        opts = {}
                
    def do_auto_seg(self, widget):
        opts = {}
        color = None
        if self.seg_black.value()!='':
            color = int(self.seg_black.value())
        opts["border_color"] = color
        opts["tolerance"] = int(self.seg_tol.value())
        opts["segmentor_class"] = seg_algos[int(self.algo.value())]
        self.seg_go.deactivate()
        self.rects = segmentate(opts, self.comix, self.page_id)[0]
        self.seg_window.hide()
        self.rects2lines()
        self.refresh_text()
        self.canvas.redraw()
        
    def auto_seg_end(self, widget):
        self.seg_window.hide()

    def text_select(self, w):
        self.selected_panel = w.value()-1
        self.canvas.redraw()

    def __init__(self, comicbook, callback):
        self.comix = comicbook
        self.callback = callback
        self.page_id = 0
        
        self.cur_data = {}
        
        self.window = Fl_Window(740, 520)
        self.window.size_range(740, 520)
        self.scroll = Fl_Scroll(10, 10, 500, 500)
        self.canvas = MyCanvas(self,10, 10, 500, 500, GridEditor)
        self.window.resizable(self.scroll)
        self.scroll.end()
        self.scroll.type(Fl_Scroll.BOTH)

        self.right = Fl_Group(520, 10, 210, 530)
        
        self.btn_left = Fl_Button(520, 10, 100, 20)
        self.btn_left.label("<< Prev Page")
        self.btn_left.callback(self.flip_back)
        self.btn_right = Fl_Button(630, 10, 100, 20)
        self.btn_right.label(">> Next Page")
        self.btn_right.callback(self.flip_fwd)
        self.spin_page = Fl_Choice(520, 30, 210, 20)
        self.spin_page.callback(self.select_page)
        for i in xrange(len(self.comix)):
            self.spin_page.add(self.comix.get_filename(i))
        self.spin_page.value(0)


        self.edit_mode_btns = Fl_Group(520, 10, 210, 70)
        self.edit_mode_btns.resizable(None)
        self.emode_label = Fl_Box(520, 55, 80, 30, "MODE:")
        self.emode_label.align(FL_ALIGN_LEFT | FL_ALIGN_INSIDE)
        self.rb_mg = Fl_Round_Button(590, 55, 60, 30, "GRID")
        self.rb_mg.mode = "g"
        self.rb_mg.type(FL_RADIO_BUTTON);
        self.rb_mg.callback(self.set_edit_mode)
        self.rb_mp = Fl_Round_Button(650, 55, 80, 30, "PANELS")
        self.rb_mp.mode = "p"
        self.rb_mp.type(FL_RADIO_BUTTON);
        self.rb_mp.callback(self.set_edit_mode)
        self.edit_mode_btns.end()

        
        self.grid_mode_btns = Fl_Group(520, 80, 210, 65)
        self.rb_h = Fl_Round_Button(520, 80, 210, 30, "edit horiz lines")
        self.rb_h.mode = "h"
        self.rb_h.type(FL_RADIO_BUTTON);
        self.rb_h.callback(self.set_grid_mode)
        self.rb_v = Fl_Round_Button(520, 100, 210, 30, "edit vert lines")
        self.rb_v.mode = "v"
        self.rb_v.type(FL_RADIO_BUTTON);
        self.rb_v.callback(self.set_grid_mode)
        self.rb_p = Fl_Round_Button(520, 120, 210, 30, "edit panels")
        self.rb_p.mode = "p"
        self.rb_p.callback(self.set_grid_mode)
        self.rb_p.type(FL_RADIO_BUTTON);
        self.grid_mode_btns.end()
        
        self.help = Fl_Multiline_Output (520, 145, 210, 60)
        self.help.box(FL_DOWN_FRAME)
        
        self.text = PanelList(self, 520, 210, 205, 225)
        self.right.resizable(self.text)
        self.text.callback(self.text_select)
        
        self.set_edit_mode(self.rb_mg)
                

        self.zooms = [(4, '25%'), (3, '33%'), (2, '50%'), (1, '100%')]

        
        self.zoom = Fl_Choice(590, 440, 140, 20, "Zoom:")
        #~ self.zoom.draw_label(520, 415, 50, 20, FL_ALIGN_LEFT)
        self.zoom.callback(self.set_zoom)
        for z in self.zooms:
            self.zoom.add(z[1])
        self.zoom.value(len(self.zooms)-1)
        self.canvas.zoom_q = 1

        self.btn_revert = Fl_Button(520, 465, 65, 20)
        self.btn_revert.label("Revert")
        self.btn_revert.callback(self.revert_segment)
        self.btn_clear = Fl_Button(595, 465, 65, 20)
        self.btn_clear.label("Clear all")
        self.btn_clear.callback(self.clear_segment)
        self.btn_auto = Fl_Button(670, 465, 60, 20)
        self.btn_auto.label("Auto")
        self.btn_auto.callback(self.auto_segment)

        
        self.btn_save = Fl_Button(520, 490, 210, 20)
        self.btn_save.label("DONE")
        self.btn_save.callback(self.done)

        self.window.end()
        self.window.set_modal()
        Fl.visual(FL_RGB)

        self.load_segmentation()
        self.selected_panel = None

        self.window.show(["Comic Watcher - segmentation editor"])
        self.saved = {}
        Fl.run()
        

if __name__=="__main__":
    try:
        import debug_scripts
    except ImportError:
        debug_scripts = False
    if debug_scripts:
        debug_scripts.go()
