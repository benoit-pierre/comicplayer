#!/usr/bin/env python

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

from fltk import *
import sys
import os.path

from seg_editor import SegEditorApp
from comic_book import ComicBook, RarComicBook, ZipComicBook, DirComicBook
from auto_segment import segmentate, seg_algos
from displayer import DisplayerApp

import threading

class MyWindow(Fl_Window):
    def draw(self):
        Fl_Window.draw(self)

class App:
    def open_file(self, widget):
        newpath = fl_file_chooser("Open Comic File", "CBZ Files (*.cbz)\tCBR Files (*.cbr)\tJPEG Files (*.jpg)\tPNG Files (*.png)\tGIF Files (*.gif)\tAll Files (*)", None)
        if newpath == None:
            return
        self.lastpath = newpath
        self.pathbox.value(self.lastpath)
        self.comix = ComicBook(self.lastpath)
        self.btn_segment.activate()
        self.btn_seg_edit.activate()
        self.btn_play.activate()        
        self.refresh_info()
        
    def open_dir(self, widget):
        newpath = fl_dir_chooser("Open Comic Folder", None)
        if newpath == None:
            return
        self.lastpath = newpath
        self.pathbox.value(self.lastpath)
        self.comix = ComicBook(self.lastpath)
        self.btn_segment.activate()
        self.btn_seg_edit.activate()
        self.btn_play.activate()        
        self.refresh_info()

    def check_writability(self):
        if self.comix.writable:
            return True
        msg = 'The comic archive file you have opened is not writable.\n'
        if type(self.comix) in [RarComicBook, ZipComicBook]:
            msg += '(CWatcher do not support archive file writing yet)\n'
        msg +='To change segmentation info, you need to convert it to a writable form.'
        res = fl_choice(msg, 'Cancel', 'Extract to directory', None)
        if res == 1:
            newcomix = DirComicBook.create_copy(fl_dir_chooser("Specify a directory", os.path.splitext(self.lastpath)[0]), self.comix)
            self.comix = newcomix
            self.pathbox.value(newcomix.path)
            self.refresh_info()
            return True
        return False


    def auto_seg(self, widget):
        if self.check_writability():
            self.seg_window = Fl_Window(500, 160)
            self.seg_progress = Fl_Progress(20, 10, 460, 20)
            self.seg_progress.minimum(0)
            self.seg_progress.maximum(len(self.comix))
            self.seg_algo = Fl_Choice(250, 40, 200, 20, "Segmentation algorithm")
            for c in seg_algos:
                self.seg_algo.add(c.__name__)
            self.seg_algo.value(0)
            self.seg_border = Fl_Choice(250, 60, 120, 20, "Border color")
            for c in self.border_choices:
                self.seg_border.add(c[0])
            self.seg_border.value(0)
            self.seg_tol = Fl_Input(250, 80, 100, 20, "Border tolerance")
            self.seg_tol.value("30")
            self.seg_min_frame = Fl_Input(250, 100, 100, 20, "Minimum frame size")
            self.seg_min_frame.value("200")
            self.seg_go = Fl_Button(170, 130, 70, 20, "GO")
            self.seg_go.callback(self.do_auto_seg)
            self.seg_cancel = Fl_Button(260, 130, 70, 20, "Cancel")
            self.seg_cancel.callback(self.auto_seg_end)
            self.seg_window.end()
            self.seg_window.set_modal()
            self.seg_window.show(["Automatic segmentation"])
            opts = {}
        
    def do_auto_seg(self, widget):
        opts = {}
        opts["border_color"] = self.border_choices[int(self.seg_border.value())][1]
        opts["tolerance"] = int(self.seg_tol.value())
        opts["segmentor_class"] = seg_algos[int(self.seg_algo.value())]
        opts["min_frame_size"] = int(self.seg_min_frame.value())
        self.seg_go.deactivate()
        for i in range(len(self.comix)):
            panels = segmentate(opts, self.comix, i, '.')
            self.comix.save_panels(i, panels[0], "rect")
            self.aseg_upd_progress('')
            Fl.wait(0)
        self.seg_window.hide()
        self.refresh_info()
        
        
    def aseg_upd_progress(self, fn):
        cur = self.seg_progress.value()
        self.seg_progress.value(cur+1)

    def auto_seg_end(self, widget):
        self.seg_window.hide()
        self.refresh_info()
        
    def seg_editor(self, widget):
        if self.check_writability():
            SegEditorApp(self.comix, self.seg_editor_end)
        self.refresh_info()

    def seg_editor_end(self):
        self.refresh_info()

    def play(self, widget):
        self.window.hide()
        app = DisplayerApp(self.comix)
        app.run()
        self.window.show()

    def play_end(self):
        self.refresh_info()
        
    def refresh_info(self):
        num = len(self.comix.filenames)
        if self.comix==None:
            self.comic_info.value("")
            return
        has_seg = "no"
        if self.comix.has_segmentation:
            has_seg = "has"
        self.comic_info.redraw()
        self.comic_info.value("%s - %s files, %s segmentation" % (self.comix.__class__.__name__, num, has_seg))
        

    def __init__(self):
        self.border_choices = [("Autodetect", None), ("Force black", 0), ("Force white", 255)]
        self.lastpath = ""
        self.window = MyWindow(520,180)
        self.pathbox = Fl_Input(60,20,240,20, "Comic: ")
        self.pathbox.value('<none selected>')
        self.btn_openf = Fl_Button(310,20,80,20, "Open file")
        self.btn_opend = Fl_Button(400,20,110,20, "Open directory")

        self.btn_openf.callback(self.open_file)
        self.btn_opend.callback(self.open_dir)

        self.btn_segment = Fl_Button(30,140,155,20, "Auto segmentation")
        self.btn_seg_edit = Fl_Button(200,140,150,20, "Edit segmentation")
        self.btn_play = Fl_Button(365,140,115,20, "Watch comic")
        
        self.comic_info = Fl_Multiline_Output(10,50,500,20)
        self.comic_info.box(FL_DOWN_BOX)
        self.comic_info.color(FL_BACKGROUND_COLOR)
        
        self.btn_segment.callback(self.auto_seg)
        self.btn_seg_edit.callback(self.seg_editor)
        self.btn_play.callback(self.play)

        self.btn_segment.deactivate()
        self.btn_seg_edit.deactivate()
        self.btn_play.deactivate()

        self.window.end()
        Fl.visual(FL_RGB)

        self.window.show(["Comic Watcher GUI"])
        Fl.run()

app = App()
