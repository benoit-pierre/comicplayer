=== Comic Player v 0.3 - brief manual ===


QUICK INTRO
===========

The purpose of this application is simple.

It is not very convenient to read a comic (either scanned or digitally drawn) on a regular computer display. 
Usually vertical resolution is unsatisfactory and you have to zoom it (quality sucks) or scroll it (irritating).

This program can segment a comic page into individual panels and highlight them one by one (or row by row),
allowing you to navigate between them using the keyboard. Segmentation is performed automatically (via some quite dumb
and slow algorithm), but you can fix/adjust it manually.


SUPPORTED PLATFORMS
===================

Windows (XP, Vista - tested; 2000, 7 - should work; NT, 9x - not sure and you should abandon them anyway)

Linux (Debian Squeeze, Ubuntu 9.10 - tested and already have all necessary compiled packages; with other distros you are on your own)

INSTALLATION INSTRUCTIONS
=========================

Ubuntu or Debian Linux
----------------------

Switch to root and issue the following commands:

> apt-get install python-setuptools python-imaging python-fltk python-pygame unrar
> easy_install pyunrar2

You should be all set. Launch the application by issuing:

> cd <directory_with_this_readme>/src
> ./cplayer.py


Windows, using prebuilt package
-------------------------------

Download a prebuilt package and unzip it.

If you do not have Python 2.6 or later installed, chances are you need msvcr90.dll (a.k.a. "MS VS 2008 redistributable").
You can get it here:
http://www.microsoft.com/downloads/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en

Go to the folder where you unzipped the prebuilt package to and launch cplayer.exe 


Windows, from source
--------------------

Install Python 2.x (http://python.org/download/), version 2.6 is recommended at the moment

Install setuptools package (http://pypi.python.org/pypi/setuptools)

Open Command Line window, change directory to C:\Python26\Scripts (or wherever you have installed Python)

Issue the following command:

easy_install PIL pyunrar2

Since Windows builds of pyFLTK and pygame have setuptools support broken at the moment,
you will need to install them separately from their respective web sites:

    http://sourceforge.net/projects/pyfltk/files/

    http://www.pygame.org/download.shtml

You also need to have msvcr71.dll in your "WINDOWS\system32" folder,
Chances are, you already do.
If not - you can install it as a part of .Net framework:

    http://www.microsoft.com/downloads/details.aspx?FamilyId=262D25E3-F589-4842-8157-034D1E7CF3A3&displaylang=en

and copy it manually from "WINDOWS\Microsoft.NET\Framework\v1.1.4322" to "WINDOWS\system32"
... or download it from any other trusted source, for example:

    http://www.dll-files.com/dllindex/dll-files.shtml?msvcr71

Go to a folder where you have downloaded comicplayer, go to subfolder "src", launch cplayer.py

BASIC USAGE
===========

The workflow is like this:

1. Open a comic book (either a folder with image files or .cbz / .cbr file).

2. Perform the auto-segmentation (if you didn't before).

3. Start watching the comic and review the auto-segmentation results.

4. If auto-segmentation failed (comic has too complex layout) or you are planning to cleanup segmentation 
    to give it away to somebody - launch a segmentation editor and correct it.


FEEDBACK
========

Feel free to report your feedback.

Project page: http://code.google.com/p/comicplayer/

Author email: yk4ever@gmail.com

