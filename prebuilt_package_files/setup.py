from distutils.core import setup
import py2exe

setup(windows=['cplayer.py'], data_files=['unrar.dll','freesansbold.ttf'])
