#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk


from libs.comic_book import ComicBook
import libs.displayer

import sys, os, os.path

if sys.platform=="win32":
    running_from_source = True
    os.environ["MAGICK_CODER_MODULE_PATH"]="."
    try:
        os.chdir("building_on_windows\\dlls")
    except OSError:
        running_from_source = False
    import libs.gm_wrap_win as gm_wrap
    libs.displayer.init_gm(gm_wrap)
    if running_from_source:
        os.chdir("..")
else:
    import libs.gm_wrap as gm_wrap
    libs.displayer.init_gm(gm_wrap)

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
        num = len(self.comix.filenames)
        self.btn_play.set_sensitive(num>0)

    def open_file(self, widget, data=None):
        buttons = (
            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK
        )
        filesel = gtk.FileChooserDialog(title="Open a comic book file", parent=self.window, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=buttons)
        fltr = gtk.FileFilter()
        fltr.add_pattern("*.cbz")
        fltr.add_pattern("*.cbr")
        fltr.add_pattern("*.CBZ")
        fltr.add_pattern("*.CBR")
        fltr.set_name("Comicbook archives (.CBZ, .CBR)")
        filesel.add_filter(fltr)
        filesel.run()
        self.path = filesel.get_filename()
        filesel.destroy()
        self.comix = ComicBook(self.path)
        self.refresh_info()
        num = len(self.comix.filenames)
        self.btn_play.set_sensitive(num>0)


    def refresh_info(self):
        if self.comix==None:
            self.comic_info.value("")
            return
        num = len(self.comix.filenames)
        self.comic_info.set_text("\"%s\", %s pages" % (self.comix.pretty_name, num))
        
    def play(self, widget, data=None):
        dapp = libs.displayer.DisplayerApp(self.comix, denoise_jpeg=self.denoise_jpeg.get_active())
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
        self.window.set_default_size(640, 240)

        vbox = gtk.VBox(homogeneous=False, spacing=0)
        self.window.add(vbox)


        hbox = gtk.HBox(homogeneous=False, spacing=0)

        self.btn_open_file = gtk.Button("Open file")
        self.btn_open_file.connect("clicked", self.open_file, None)
        hbox.pack_start(self.btn_open_file)

        self.btn_open_dir = gtk.Button("Open folder")
        self.btn_open_dir.connect("clicked", self.open_dir, None)
        hbox.pack_end(self.btn_open_dir)
        
        vbox.pack_start(hbox, expand=False)
        
        self.comic_info = gtk.Label("No comic loaded")
        vbox.pack_start(self.comic_info, expand=False, padding=8)

        self.btn_play = gtk.Button("Watch comic")
        self.btn_play.connect("clicked", self.play, None)
        self.btn_play.set_sensitive(False)
        vbox.pack_start(self.btn_play, expand=False)
        
        hsep = gtk.HSeparator()
        vbox.pack_start(hsep, padding=10, expand=False)

        seg_opts = gtk.Label("Displaying options:")
        seg_opts.set_alignment(0, 0)
        vbox.pack_start(seg_opts, expand=False)
        
        self.denoise_jpeg = gtk.CheckButton(label="Denoise low-quality JPEG images")
        self.denoise_jpeg.set_alignment(0.2, 0)
        self.denoise_jpeg.set_active(True)
        vbox.pack_start(self.denoise_jpeg, expand=False)

        self.ignore_small_rows = gtk.CheckButton(label="Ignore small non-blank parts of the page")
        self.ignore_small_rows.set_alignment(0.2, 0)
        self.ignore_small_rows.set_active(True)
        vbox.pack_start(self.ignore_small_rows, expand=False)


        self.btn_open_dir.show()
        self.btn_open_file.show()
        self.btn_play.show()
        self.comic_info.show()
        self.denoise_jpeg.show()
        self.ignore_small_rows.show()
        hsep.show()
        seg_opts.show()
        hbox.show()
        vbox.show()
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    app = ComicPlayer()
    app.main()





