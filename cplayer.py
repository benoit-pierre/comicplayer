#!/usr/bin/env python

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

from fltk import *
import sys
import os.path

from libs.comic_book import ComicBook, RarComicBook, ZipComicBook, DirComicBook
from libs.displayer import DisplayerApp

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
        self.btn_play.activate()        
        self.refresh_info()
        
    def open_dir(self, widget):
        newpath = fl_dir_chooser("Open Comic Folder", None)
        if newpath == None:
            return
        self.lastpath = newpath
        self.pathbox.value(self.lastpath)
        self.comix = ComicBook(self.lastpath)
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
        self.border_thick_choices = [("1 px", 1), ("3 px square", 3), ("5 px square", 5)]
        self.lastpath = ""
        self.window = MyWindow(520,180)
        self.pathbox = Fl_Input(60,20,240,20, "Comic: ")
        self.pathbox.value('<none selected>')
        self.btn_openf = Fl_Button(310,20,80,20, "Open file")
        self.btn_opend = Fl_Button(400,20,110,20, "Open directory")

        self.btn_openf.callback(self.open_file)
        self.btn_opend.callback(self.open_dir)

        self.btn_play = Fl_Button(30,140,450,20, "Watch comic")
        
        self.comic_info = Fl_Multiline_Output(10,50,500,20)
        self.comic_info.box(FL_DOWN_BOX)
        self.comic_info.color(FL_BACKGROUND_COLOR)
        
        self.btn_play.callback(self.play)

        self.btn_play.deactivate()

        self.window.end()
        Fl.visual(FL_RGB)

        self.window.show(["Comic Watcher GUI"])
        Fl.run()

app = App()
