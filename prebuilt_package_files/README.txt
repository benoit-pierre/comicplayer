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

To use this application in Linux - use source download


INSTALLATION INSTRUCTIONS - Windows, using prebuilt package
===========================================================

Download a prebuilt package and unzip it (if you are reading this, you are probably past that step)

If you do not have Python 2.6 or later installed, chances are you need msvcr90.dll (a.k.a. "MS VS 2008 redistributable").
You can get it here:
http://www.microsoft.com/downloads/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en

Go to the folder where you unzipped the prebuilt package to and launch cplayer.exe 


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

