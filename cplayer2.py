#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk

import sys
import os.path

from libs.comic_book import ComicBook, RarComicBook, ZipComicBook, DirComicBook
from libs.displayer import DisplayerApp

class ComicPlayer:

    def open_dir(self, widget, data=None):
        buttons = (
            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK
        )
        filesel = gtk.FileChooserDialog(title="Open a comic book folder", parent=self.window, action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=buttons)
        filesel.run()
        self.path = filesel.get_filename()
        filesel.destroy()
        self.comix = ComicBook(self.path)
        self.refresh_info()

    def refresh_info(self):
        num = len(self.comix.filenames)
        if self.comix==None:
            self.comic_info.value("")
            return
        has_seg = "no"
        if self.comix.has_segmentation:
            has_seg = "has"
        self.comic_info.set_text("%s - %s files, %s segmentation" % (self.comix.__class__.__name__, num, has_seg))
        
    def play(self, widget, data=None):
        dapp = DisplayerApp(self.comix)
        dapp.run()
        

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        vbox = gtk.VBox(homogeneous=False, spacing=0)
        self.window.add(vbox)

        self.btn_open_dir = gtk.Button("Open a comic book folder")
        self.btn_open_dir.connect("clicked", self.open_dir, None)
        vbox.pack_start(self.btn_open_dir)
        
        self.comic_info = gtk.Label("No comic loaded")
        vbox.pack_start(self.comic_info)

        self.btn_play = gtk.Button("Watch comic")
        self.btn_play.connect("clicked", self.play, None)
        vbox.pack_end(self.btn_play)


        self.btn_open_dir.show()
        self.btn_play.show()
        self.comic_info.show()
        vbox.show()
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    app = ComicPlayer()
    app.main()
