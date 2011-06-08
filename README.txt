=== Comic Player v 0.4 ===
=== manual for SOURCE DISTRIBUTION ===


QUICK INTRO
===========

The purpose of this application is simple.

It is not very convenient to read a comic (either scanned or digitally drawn) on a regular 
computer display. Usually vertical resolution is unsatisfactory and you have to zoom it (quality 
loss) or scroll it (irritating). Also, scanned comics are often of inferior quality.

This program can segment a comic page into "rows" and easily scroll between them using keyboard. 
Segmentation is performed automatically.

Also, source files are enhanced and automatically zoomed to fit in the monitor optimally.


SUPPORTED PLATFORMS
===================

Windows (XP, Vista - tested; 2000, 7 - should work). You might want to use prebuilt binary 
distribution instead.

Linux (Ubuntu 11.04/Linux Mint 11) - tested and should work.


INSTALLATION INSTRUCTIONS
=========================

Ubuntu or Debian Linux
----------------------

Switch to root and issue the following commands:

> apt-get install python-setuptools python-imaging python-gtk2 python-pygame unrar libgraphicsmagick3
> easy_install pyunrar2

You should be all set. Launch the application by issuing:

> cd <directory_with_this_readme>/src
> ./cplayer.py


Windows
-------

Install Python 2.x (http://python.org/download/), version 2.7 is recommended at the moment

Install the following packages:
(NOTE - if you are an experienced Python user, you can try to use easy_install script from 
setuptools)

PIL - from http://www.pythonware.com/products/pil/
pyunrar2 - from http://code.google.com/p/py-unrar2/downloads/list
pygtk (all-in-one bundle) - from http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.24/
pygame - from http://pygame.org/ftp/

Go to a folder where you have downloaded comicplayer, go to subfolder "src", launch cplayer.py


BASIC USAGE
===========

The workflow is like this:

1. Open a comic book (either a folder with image files or .cbz / .cbr file).

2. Start reading the comic.


FEEDBACK
========

Feel free to report your feedback.

Project page: http://code.google.com/p/comicplayer/

Author email: yk4ever@gmail.com

