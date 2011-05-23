'''Wrapper for image.h

Generated with:
/home/rainman/projects/ctypesgen-read-only/ctypesgen.py -lGraphicsMagick -llcms -ltiff -lfreetype -ljasper -ljpeg -lpng -lwmflite -lXext -lSM -lICE -lX11 -lbz2 -lxml2 -lz -lm -lgomp -lpthread -lltdl gmagick_hdrs/magick/image.h gmagick_hdrs/magick/magick.h gmagick_hdrs/magick/error.h gmagick_hdrs/magick/constitute.h gmagick_hdrs/magick/resize.h gmagick_hdrs/magick/delegate.h gmagick_hdrs/magick/effect.h gmagick_hdrs/magick/enhance.h gmagick_hdrs/magick/pixel_cache.h gmagick_hdrs/magick/blob.h gmagick_hdrs/magick/attribute.h -o gm_wrap.py -I gmagick_hdrs/

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname

        else:
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries

_libs["GraphicsMagick"] = load_library("GraphicsMagick")
_libs["lcms"] = load_library("lcms")
_libs["tiff"] = load_library("tiff")
_libs["freetype"] = load_library("freetype")
_libs["jasper"] = load_library("jasper")
_libs["jpeg"] = load_library("jpeg")
_libs["png"] = load_library("png")
_libs["wmflite"] = load_library("wmflite")
_libs["Xext"] = load_library("Xext")
_libs["SM"] = load_library("SM")
_libs["ICE"] = load_library("ICE")
_libs["X11"] = load_library("X11")
_libs["bz2"] = load_library("bz2")
_libs["xml2"] = load_library("xml2")
_libs["z"] = load_library("z")
_libs["m"] = load_library("m")
_libs["gomp"] = load_library("gomp")
_libs["pthread"] = load_library("pthread")
_libs["ltdl"] = load_library("ltdl")

# 19 libraries
# End libraries

# No modules

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 553
class struct__Image(Structure):
    pass

# gmagick_hdrs/magick/forward.h: 20
class struct__Ascii85Info(Structure):
    pass

_Ascii85InfoPtr_ = POINTER(struct__Ascii85Info) # gmagick_hdrs/magick/forward.h: 20

# gmagick_hdrs/magick/forward.h: 22
class struct__BlobInfo(Structure):
    pass

_BlobInfoPtr_ = POINTER(struct__BlobInfo) # gmagick_hdrs/magick/forward.h: 22

# gmagick_hdrs/magick/forward.h: 24
class struct__CacheInfo(Structure):
    pass

_CacheInfoPtr_ = POINTER(struct__CacheInfo) # gmagick_hdrs/magick/forward.h: 24

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/attribute.h: 20
class struct__ImageAttribute(Structure):
    pass

_ImageAttributePtr_ = POINTER(struct__ImageAttribute) # gmagick_hdrs/magick/forward.h: 26

# gmagick_hdrs/magick/forward.h: 28
class struct__SemaphoreInfo(Structure):
    pass

_SemaphoreInfoPtr_ = POINTER(struct__SemaphoreInfo) # gmagick_hdrs/magick/forward.h: 28

# gmagick_hdrs/magick/forward.h: 30
class struct__ThreadViewSet(Structure):
    pass

_ThreadViewSetPtr_ = POINTER(struct__ThreadViewSet) # gmagick_hdrs/magick/forward.h: 30

ViewInfo = POINTER(None) # gmagick_hdrs/magick/forward.h: 32

Quantum = c_ubyte # gmagick_hdrs/magick/magick_config.h: 38

enum_anon_1 = c_int # gmagick_hdrs/magick/colorspace.h: 113

ColorspaceType = enum_anon_1 # gmagick_hdrs/magick/colorspace.h: 113

enum_anon_2 = c_int # gmagick_hdrs/magick/error.h: 58

UndefinedExceptionBase = 0 # gmagick_hdrs/magick/error.h: 58

ExceptionBase = 1 # gmagick_hdrs/magick/error.h: 58

ResourceBase = 2 # gmagick_hdrs/magick/error.h: 58

ResourceLimitBase = 2 # gmagick_hdrs/magick/error.h: 58

TypeBase = 5 # gmagick_hdrs/magick/error.h: 58

AnnotateBase = 5 # gmagick_hdrs/magick/error.h: 58

OptionBase = 10 # gmagick_hdrs/magick/error.h: 58

DelegateBase = 15 # gmagick_hdrs/magick/error.h: 58

MissingDelegateBase = 20 # gmagick_hdrs/magick/error.h: 58

CorruptImageBase = 25 # gmagick_hdrs/magick/error.h: 58

FileOpenBase = 30 # gmagick_hdrs/magick/error.h: 58

BlobBase = 35 # gmagick_hdrs/magick/error.h: 58

StreamBase = 40 # gmagick_hdrs/magick/error.h: 58

CacheBase = 45 # gmagick_hdrs/magick/error.h: 58

CoderBase = 50 # gmagick_hdrs/magick/error.h: 58

ModuleBase = 55 # gmagick_hdrs/magick/error.h: 58

DrawBase = 60 # gmagick_hdrs/magick/error.h: 58

RenderBase = 60 # gmagick_hdrs/magick/error.h: 58

ImageBase = 65 # gmagick_hdrs/magick/error.h: 58

WandBase = 67 # gmagick_hdrs/magick/error.h: 58

TemporaryFileBase = 70 # gmagick_hdrs/magick/error.h: 58

TransformBase = 75 # gmagick_hdrs/magick/error.h: 58

XServerBase = 80 # gmagick_hdrs/magick/error.h: 58

X11Base = 81 # gmagick_hdrs/magick/error.h: 58

UserBase = 82 # gmagick_hdrs/magick/error.h: 58

MonitorBase = 85 # gmagick_hdrs/magick/error.h: 58

LocaleBase = 86 # gmagick_hdrs/magick/error.h: 58

DeprecateBase = 87 # gmagick_hdrs/magick/error.h: 58

RegistryBase = 90 # gmagick_hdrs/magick/error.h: 58

ConfigureBase = 95 # gmagick_hdrs/magick/error.h: 58

ExceptionBaseType = enum_anon_2 # gmagick_hdrs/magick/error.h: 58

enum_anon_3 = c_int # gmagick_hdrs/magick/error.h: 186

UndefinedException = 0 # gmagick_hdrs/magick/error.h: 186

EventException = 100 # gmagick_hdrs/magick/error.h: 186

ExceptionEvent = (EventException + ExceptionBase) # gmagick_hdrs/magick/error.h: 186

ResourceEvent = (EventException + ResourceBase) # gmagick_hdrs/magick/error.h: 186

ResourceLimitEvent = (EventException + ResourceLimitBase) # gmagick_hdrs/magick/error.h: 186

TypeEvent = (EventException + TypeBase) # gmagick_hdrs/magick/error.h: 186

AnnotateEvent = (EventException + AnnotateBase) # gmagick_hdrs/magick/error.h: 186

OptionEvent = (EventException + OptionBase) # gmagick_hdrs/magick/error.h: 186

DelegateEvent = (EventException + DelegateBase) # gmagick_hdrs/magick/error.h: 186

MissingDelegateEvent = (EventException + MissingDelegateBase) # gmagick_hdrs/magick/error.h: 186

CorruptImageEvent = (EventException + CorruptImageBase) # gmagick_hdrs/magick/error.h: 186

FileOpenEvent = (EventException + FileOpenBase) # gmagick_hdrs/magick/error.h: 186

BlobEvent = (EventException + BlobBase) # gmagick_hdrs/magick/error.h: 186

StreamEvent = (EventException + StreamBase) # gmagick_hdrs/magick/error.h: 186

CacheEvent = (EventException + CacheBase) # gmagick_hdrs/magick/error.h: 186

CoderEvent = (EventException + CoderBase) # gmagick_hdrs/magick/error.h: 186

ModuleEvent = (EventException + ModuleBase) # gmagick_hdrs/magick/error.h: 186

DrawEvent = (EventException + DrawBase) # gmagick_hdrs/magick/error.h: 186

RenderEvent = (EventException + RenderBase) # gmagick_hdrs/magick/error.h: 186

ImageEvent = (EventException + ImageBase) # gmagick_hdrs/magick/error.h: 186

WandEvent = (EventException + WandBase) # gmagick_hdrs/magick/error.h: 186

TemporaryFileEvent = (EventException + TemporaryFileBase) # gmagick_hdrs/magick/error.h: 186

TransformEvent = (EventException + TransformBase) # gmagick_hdrs/magick/error.h: 186

XServerEvent = (EventException + XServerBase) # gmagick_hdrs/magick/error.h: 186

X11Event = (EventException + X11Base) # gmagick_hdrs/magick/error.h: 186

UserEvent = (EventException + UserBase) # gmagick_hdrs/magick/error.h: 186

MonitorEvent = (EventException + MonitorBase) # gmagick_hdrs/magick/error.h: 186

LocaleEvent = (EventException + LocaleBase) # gmagick_hdrs/magick/error.h: 186

DeprecateEvent = (EventException + DeprecateBase) # gmagick_hdrs/magick/error.h: 186

RegistryEvent = (EventException + RegistryBase) # gmagick_hdrs/magick/error.h: 186

ConfigureEvent = (EventException + ConfigureBase) # gmagick_hdrs/magick/error.h: 186

WarningException = 300 # gmagick_hdrs/magick/error.h: 186

ExceptionWarning = (WarningException + ExceptionBase) # gmagick_hdrs/magick/error.h: 186

ResourceWarning = (WarningException + ResourceBase) # gmagick_hdrs/magick/error.h: 186

ResourceLimitWarning = (WarningException + ResourceLimitBase) # gmagick_hdrs/magick/error.h: 186

TypeWarning = (WarningException + TypeBase) # gmagick_hdrs/magick/error.h: 186

AnnotateWarning = (WarningException + AnnotateBase) # gmagick_hdrs/magick/error.h: 186

OptionWarning = (WarningException + OptionBase) # gmagick_hdrs/magick/error.h: 186

DelegateWarning = (WarningException + DelegateBase) # gmagick_hdrs/magick/error.h: 186

MissingDelegateWarning = (WarningException + MissingDelegateBase) # gmagick_hdrs/magick/error.h: 186

CorruptImageWarning = (WarningException + CorruptImageBase) # gmagick_hdrs/magick/error.h: 186

FileOpenWarning = (WarningException + FileOpenBase) # gmagick_hdrs/magick/error.h: 186

BlobWarning = (WarningException + BlobBase) # gmagick_hdrs/magick/error.h: 186

StreamWarning = (WarningException + StreamBase) # gmagick_hdrs/magick/error.h: 186

CacheWarning = (WarningException + CacheBase) # gmagick_hdrs/magick/error.h: 186

CoderWarning = (WarningException + CoderBase) # gmagick_hdrs/magick/error.h: 186

ModuleWarning = (WarningException + ModuleBase) # gmagick_hdrs/magick/error.h: 186

DrawWarning = (WarningException + DrawBase) # gmagick_hdrs/magick/error.h: 186

RenderWarning = (WarningException + RenderBase) # gmagick_hdrs/magick/error.h: 186

ImageWarning = (WarningException + ImageBase) # gmagick_hdrs/magick/error.h: 186

WandWarning = (WarningException + WandBase) # gmagick_hdrs/magick/error.h: 186

TemporaryFileWarning = (WarningException + TemporaryFileBase) # gmagick_hdrs/magick/error.h: 186

TransformWarning = (WarningException + TransformBase) # gmagick_hdrs/magick/error.h: 186

XServerWarning = (WarningException + XServerBase) # gmagick_hdrs/magick/error.h: 186

X11Warning = (WarningException + X11Base) # gmagick_hdrs/magick/error.h: 186

UserWarning = (WarningException + UserBase) # gmagick_hdrs/magick/error.h: 186

MonitorWarning = (WarningException + MonitorBase) # gmagick_hdrs/magick/error.h: 186

LocaleWarning = (WarningException + LocaleBase) # gmagick_hdrs/magick/error.h: 186

DeprecateWarning = (WarningException + DeprecateBase) # gmagick_hdrs/magick/error.h: 186

RegistryWarning = (WarningException + RegistryBase) # gmagick_hdrs/magick/error.h: 186

ConfigureWarning = (WarningException + ConfigureBase) # gmagick_hdrs/magick/error.h: 186

ErrorException = 400 # gmagick_hdrs/magick/error.h: 186

ExceptionError = (ErrorException + ExceptionBase) # gmagick_hdrs/magick/error.h: 186

ResourceError = (ErrorException + ResourceBase) # gmagick_hdrs/magick/error.h: 186

ResourceLimitError = (ErrorException + ResourceLimitBase) # gmagick_hdrs/magick/error.h: 186

TypeError = (ErrorException + TypeBase) # gmagick_hdrs/magick/error.h: 186

AnnotateError = (ErrorException + AnnotateBase) # gmagick_hdrs/magick/error.h: 186

OptionError = (ErrorException + OptionBase) # gmagick_hdrs/magick/error.h: 186

DelegateError = (ErrorException + DelegateBase) # gmagick_hdrs/magick/error.h: 186

MissingDelegateError = (ErrorException + MissingDelegateBase) # gmagick_hdrs/magick/error.h: 186

CorruptImageError = (ErrorException + CorruptImageBase) # gmagick_hdrs/magick/error.h: 186

FileOpenError = (ErrorException + FileOpenBase) # gmagick_hdrs/magick/error.h: 186

BlobError = (ErrorException + BlobBase) # gmagick_hdrs/magick/error.h: 186

StreamError = (ErrorException + StreamBase) # gmagick_hdrs/magick/error.h: 186

CacheError = (ErrorException + CacheBase) # gmagick_hdrs/magick/error.h: 186

CoderError = (ErrorException + CoderBase) # gmagick_hdrs/magick/error.h: 186

ModuleError = (ErrorException + ModuleBase) # gmagick_hdrs/magick/error.h: 186

DrawError = (ErrorException + DrawBase) # gmagick_hdrs/magick/error.h: 186

RenderError = (ErrorException + RenderBase) # gmagick_hdrs/magick/error.h: 186

ImageError = (ErrorException + ImageBase) # gmagick_hdrs/magick/error.h: 186

WandError = (ErrorException + WandBase) # gmagick_hdrs/magick/error.h: 186

TemporaryFileError = (ErrorException + TemporaryFileBase) # gmagick_hdrs/magick/error.h: 186

TransformError = (ErrorException + TransformBase) # gmagick_hdrs/magick/error.h: 186

XServerError = (ErrorException + XServerBase) # gmagick_hdrs/magick/error.h: 186

X11Error = (ErrorException + X11Base) # gmagick_hdrs/magick/error.h: 186

UserError = (ErrorException + UserBase) # gmagick_hdrs/magick/error.h: 186

MonitorError = (ErrorException + MonitorBase) # gmagick_hdrs/magick/error.h: 186

LocaleError = (ErrorException + LocaleBase) # gmagick_hdrs/magick/error.h: 186

DeprecateError = (ErrorException + DeprecateBase) # gmagick_hdrs/magick/error.h: 186

RegistryError = (ErrorException + RegistryBase) # gmagick_hdrs/magick/error.h: 186

ConfigureError = (ErrorException + ConfigureBase) # gmagick_hdrs/magick/error.h: 186

FatalErrorException = 700 # gmagick_hdrs/magick/error.h: 186

ExceptionFatalError = (FatalErrorException + ExceptionBase) # gmagick_hdrs/magick/error.h: 186

ResourceFatalError = (FatalErrorException + ResourceBase) # gmagick_hdrs/magick/error.h: 186

ResourceLimitFatalError = (FatalErrorException + ResourceLimitBase) # gmagick_hdrs/magick/error.h: 186

TypeFatalError = (FatalErrorException + TypeBase) # gmagick_hdrs/magick/error.h: 186

AnnotateFatalError = (FatalErrorException + AnnotateBase) # gmagick_hdrs/magick/error.h: 186

OptionFatalError = (FatalErrorException + OptionBase) # gmagick_hdrs/magick/error.h: 186

DelegateFatalError = (FatalErrorException + DelegateBase) # gmagick_hdrs/magick/error.h: 186

MissingDelegateFatalError = (FatalErrorException + MissingDelegateBase) # gmagick_hdrs/magick/error.h: 186

CorruptImageFatalError = (FatalErrorException + CorruptImageBase) # gmagick_hdrs/magick/error.h: 186

FileOpenFatalError = (FatalErrorException + FileOpenBase) # gmagick_hdrs/magick/error.h: 186

BlobFatalError = (FatalErrorException + BlobBase) # gmagick_hdrs/magick/error.h: 186

StreamFatalError = (FatalErrorException + StreamBase) # gmagick_hdrs/magick/error.h: 186

CacheFatalError = (FatalErrorException + CacheBase) # gmagick_hdrs/magick/error.h: 186

CoderFatalError = (FatalErrorException + CoderBase) # gmagick_hdrs/magick/error.h: 186

ModuleFatalError = (FatalErrorException + ModuleBase) # gmagick_hdrs/magick/error.h: 186

DrawFatalError = (FatalErrorException + DrawBase) # gmagick_hdrs/magick/error.h: 186

RenderFatalError = (FatalErrorException + RenderBase) # gmagick_hdrs/magick/error.h: 186

ImageFatalError = (FatalErrorException + ImageBase) # gmagick_hdrs/magick/error.h: 186

WandFatalError = (FatalErrorException + WandBase) # gmagick_hdrs/magick/error.h: 186

TemporaryFileFatalError = (FatalErrorException + TemporaryFileBase) # gmagick_hdrs/magick/error.h: 186

TransformFatalError = (FatalErrorException + TransformBase) # gmagick_hdrs/magick/error.h: 186

XServerFatalError = (FatalErrorException + XServerBase) # gmagick_hdrs/magick/error.h: 186

X11FatalError = (FatalErrorException + X11Base) # gmagick_hdrs/magick/error.h: 186

UserFatalError = (FatalErrorException + UserBase) # gmagick_hdrs/magick/error.h: 186

MonitorFatalError = (FatalErrorException + MonitorBase) # gmagick_hdrs/magick/error.h: 186

LocaleFatalError = (FatalErrorException + LocaleBase) # gmagick_hdrs/magick/error.h: 186

DeprecateFatalError = (FatalErrorException + DeprecateBase) # gmagick_hdrs/magick/error.h: 186

RegistryFatalError = (FatalErrorException + RegistryBase) # gmagick_hdrs/magick/error.h: 186

ConfigureFatalError = (FatalErrorException + ConfigureBase) # gmagick_hdrs/magick/error.h: 186

ExceptionType = enum_anon_3 # gmagick_hdrs/magick/error.h: 186

# gmagick_hdrs/magick/error.h: 230
class struct__ExceptionInfo(Structure):
    pass

struct__ExceptionInfo.__slots__ = [
    'severity',
    'reason',
    'description',
    'error_number',
    'module',
    'function',
    'line',
    'signature',
]
struct__ExceptionInfo._fields_ = [
    ('severity', ExceptionType),
    ('reason', String),
    ('description', String),
    ('error_number', c_int),
    ('module', String),
    ('function', String),
    ('line', c_ulong),
    ('signature', c_ulong),
]

ExceptionInfo = struct__ExceptionInfo # gmagick_hdrs/magick/error.h: 230

ErrorHandler = CFUNCTYPE(UNCHECKED(None), ExceptionType, String, String) # gmagick_hdrs/magick/error.h: 236

FatalErrorHandler = CFUNCTYPE(UNCHECKED(None), ExceptionType, String, String) # gmagick_hdrs/magick/error.h: 239

WarningHandler = CFUNCTYPE(UNCHECKED(None), ExceptionType, String, String) # gmagick_hdrs/magick/error.h: 242

# gmagick_hdrs/magick/error.h: 248
if hasattr(_libs['GraphicsMagick'], 'GetLocaleExceptionMessage'):
    GetLocaleExceptionMessage = _libs['GraphicsMagick'].GetLocaleExceptionMessage
    GetLocaleExceptionMessage.argtypes = [ExceptionType, String]
    if sizeof(c_int) == sizeof(c_void_p):
        GetLocaleExceptionMessage.restype = ReturnString
    else:
        GetLocaleExceptionMessage.restype = String
        GetLocaleExceptionMessage.errcheck = ReturnString

# gmagick_hdrs/magick/error.h: 248
if hasattr(_libs['GraphicsMagick'], 'GetLocaleMessage'):
    GetLocaleMessage = _libs['GraphicsMagick'].GetLocaleMessage
    GetLocaleMessage.argtypes = [String]
    if sizeof(c_int) == sizeof(c_void_p):
        GetLocaleMessage.restype = ReturnString
    else:
        GetLocaleMessage.restype = String
        GetLocaleMessage.errcheck = ReturnString

# gmagick_hdrs/magick/error.h: 252
if hasattr(_libs['GraphicsMagick'], 'SetErrorHandler'):
    SetErrorHandler = _libs['GraphicsMagick'].SetErrorHandler
    SetErrorHandler.argtypes = [ErrorHandler]
    SetErrorHandler.restype = ErrorHandler

# gmagick_hdrs/magick/error.h: 255
if hasattr(_libs['GraphicsMagick'], 'SetFatalErrorHandler'):
    SetFatalErrorHandler = _libs['GraphicsMagick'].SetFatalErrorHandler
    SetFatalErrorHandler.argtypes = [FatalErrorHandler]
    SetFatalErrorHandler.restype = FatalErrorHandler

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], 'CatchException'):
    CatchException = _libs['GraphicsMagick'].CatchException
    CatchException.argtypes = [POINTER(ExceptionInfo)]
    CatchException.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], 'CopyException'):
    CopyException = _libs['GraphicsMagick'].CopyException
    CopyException.argtypes = [POINTER(ExceptionInfo), POINTER(ExceptionInfo)]
    CopyException.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], 'DestroyExceptionInfo'):
    DestroyExceptionInfo = _libs['GraphicsMagick'].DestroyExceptionInfo
    DestroyExceptionInfo.argtypes = [POINTER(ExceptionInfo)]
    DestroyExceptionInfo.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], 'GetExceptionInfo'):
    GetExceptionInfo = _libs['GraphicsMagick'].GetExceptionInfo
    GetExceptionInfo.argtypes = [POINTER(ExceptionInfo)]
    GetExceptionInfo.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], 'MagickError'):
    MagickError = _libs['GraphicsMagick'].MagickError
    MagickError.argtypes = [ExceptionType, String, String]
    MagickError.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], 'MagickFatalError'):
    MagickFatalError = _libs['GraphicsMagick'].MagickFatalError
    MagickFatalError.argtypes = [ExceptionType, String, String]
    MagickFatalError.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], 'MagickWarning'):
    MagickWarning = _libs['GraphicsMagick'].MagickWarning
    MagickWarning.argtypes = [ExceptionType, String, String]
    MagickWarning.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], '_MagickError'):
    _MagickError = _libs['GraphicsMagick']._MagickError
    _MagickError.argtypes = [ExceptionType, String, String]
    _MagickError.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], '_MagickFatalError'):
    _MagickFatalError = _libs['GraphicsMagick']._MagickFatalError
    _MagickFatalError.argtypes = [ExceptionType, String, String]
    _MagickFatalError.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], '_MagickWarning'):
    _MagickWarning = _libs['GraphicsMagick']._MagickWarning
    _MagickWarning.argtypes = [ExceptionType, String, String]
    _MagickWarning.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], 'SetExceptionInfo'):
    SetExceptionInfo = _libs['GraphicsMagick'].SetExceptionInfo
    SetExceptionInfo.argtypes = [POINTER(ExceptionInfo), ExceptionType]
    SetExceptionInfo.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], 'ThrowException'):
    ThrowException = _libs['GraphicsMagick'].ThrowException
    ThrowException.argtypes = [POINTER(ExceptionInfo), ExceptionType, String, String]
    ThrowException.restype = None

# gmagick_hdrs/magick/error.h: 258
if hasattr(_libs['GraphicsMagick'], 'ThrowLoggedException'):
    ThrowLoggedException = _libs['GraphicsMagick'].ThrowLoggedException
    ThrowLoggedException.argtypes = [POINTER(ExceptionInfo), ExceptionType, String, String, String, String, c_ulong]
    ThrowLoggedException.restype = None

# gmagick_hdrs/magick/error.h: 275
if hasattr(_libs['GraphicsMagick'], 'SetWarningHandler'):
    SetWarningHandler = _libs['GraphicsMagick'].SetWarningHandler
    SetWarningHandler.argtypes = [WarningHandler]
    SetWarningHandler.restype = WarningHandler

enum_anon_5 = c_int # gmagick_hdrs/magick/timer.h: 26

TimerState = enum_anon_5 # gmagick_hdrs/magick/timer.h: 26

# gmagick_hdrs/magick/timer.h: 37
class struct__Timer(Structure):
    pass

struct__Timer.__slots__ = [
    'start',
    'stop',
    'total',
]
struct__Timer._fields_ = [
    ('start', c_double),
    ('stop', c_double),
    ('total', c_double),
]

Timer = struct__Timer # gmagick_hdrs/magick/timer.h: 37

# gmagick_hdrs/magick/timer.h: 50
class struct__TimerInfo(Structure):
    pass

struct__TimerInfo.__slots__ = [
    'user',
    'elapsed',
    'state',
    'signature',
]
struct__TimerInfo._fields_ = [
    ('user', Timer),
    ('elapsed', Timer),
    ('state', TimerState),
    ('signature', c_ulong),
]

TimerInfo = struct__TimerInfo # gmagick_hdrs/magick/timer.h: 50

__off_t = c_long # /usr/include/bits/types.h: 141

__off64_t = c_long # /usr/include/bits/types.h: 142

# /usr/include/libio.h: 271
class struct__IO_FILE(Structure):
    pass

FILE = struct__IO_FILE # /usr/include/stdio.h: 49

_IO_lock_t = None # /usr/include/libio.h: 180

# /usr/include/libio.h: 186
class struct__IO_marker(Structure):
    pass

struct__IO_marker.__slots__ = [
    '_next',
    '_sbuf',
    '_pos',
]
struct__IO_marker._fields_ = [
    ('_next', POINTER(struct__IO_marker)),
    ('_sbuf', POINTER(struct__IO_FILE)),
    ('_pos', c_int),
]

struct__IO_FILE.__slots__ = [
    '_flags',
    '_IO_read_ptr',
    '_IO_read_end',
    '_IO_read_base',
    '_IO_write_base',
    '_IO_write_ptr',
    '_IO_write_end',
    '_IO_buf_base',
    '_IO_buf_end',
    '_IO_save_base',
    '_IO_backup_base',
    '_IO_save_end',
    '_markers',
    '_chain',
    '_fileno',
    '_flags2',
    '_old_offset',
    '_cur_column',
    '_vtable_offset',
    '_shortbuf',
    '_lock',
    '_offset',
    '__pad1',
    '__pad2',
    '__pad3',
    '__pad4',
    '__pad5',
    '_mode',
    '_unused2',
]
struct__IO_FILE._fields_ = [
    ('_flags', c_int),
    ('_IO_read_ptr', String),
    ('_IO_read_end', String),
    ('_IO_read_base', String),
    ('_IO_write_base', String),
    ('_IO_write_ptr', String),
    ('_IO_write_end', String),
    ('_IO_buf_base', String),
    ('_IO_buf_end', String),
    ('_IO_save_base', String),
    ('_IO_backup_base', String),
    ('_IO_save_end', String),
    ('_markers', POINTER(struct__IO_marker)),
    ('_chain', POINTER(struct__IO_FILE)),
    ('_fileno', c_int),
    ('_flags2', c_int),
    ('_old_offset', __off_t),
    ('_cur_column', c_ushort),
    ('_vtable_offset', c_char),
    ('_shortbuf', c_char * 1),
    ('_lock', POINTER(_IO_lock_t)),
    ('_offset', __off64_t),
    ('__pad1', POINTER(None)),
    ('__pad2', POINTER(None)),
    ('__pad3', POINTER(None)),
    ('__pad4', POINTER(None)),
    ('__pad5', c_size_t),
    ('_mode', c_int),
    ('_unused2', c_char * (((15 * sizeof(c_int)) - (4 * sizeof(POINTER(None)))) - sizeof(c_size_t))),
]

enum_anon_11 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 75

UnspecifiedAlpha = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 75

AssociatedAlpha = (UnspecifiedAlpha + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 75

UnassociatedAlpha = (AssociatedAlpha + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 75

AlphaType = enum_anon_11 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 75

enum_anon_12 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

UndefinedChannel = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

RedChannel = (UndefinedChannel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

CyanChannel = (RedChannel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

GreenChannel = (CyanChannel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

MagentaChannel = (GreenChannel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

BlueChannel = (MagentaChannel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

YellowChannel = (BlueChannel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

OpacityChannel = (YellowChannel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

BlackChannel = (OpacityChannel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

MatteChannel = (BlackChannel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

AllChannels = (MatteChannel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

GrayChannel = (AllChannels + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

ChannelType = enum_anon_12 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 91

enum_anon_13 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 98

UndefinedClass = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 98

DirectClass = (UndefinedClass + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 98

PseudoClass = (DirectClass + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 98

ClassType = enum_anon_13 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 98

enum_anon_14 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

UndefinedCompositeOp = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

OverCompositeOp = (UndefinedCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

InCompositeOp = (OverCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

OutCompositeOp = (InCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

AtopCompositeOp = (OutCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

XorCompositeOp = (AtopCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

PlusCompositeOp = (XorCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

MinusCompositeOp = (PlusCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

AddCompositeOp = (MinusCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

SubtractCompositeOp = (AddCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

DifferenceCompositeOp = (SubtractCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

MultiplyCompositeOp = (DifferenceCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

BumpmapCompositeOp = (MultiplyCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

CopyCompositeOp = (BumpmapCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

CopyRedCompositeOp = (CopyCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

CopyGreenCompositeOp = (CopyRedCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

CopyBlueCompositeOp = (CopyGreenCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

CopyOpacityCompositeOp = (CopyBlueCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

ClearCompositeOp = (CopyOpacityCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

DissolveCompositeOp = (ClearCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

DisplaceCompositeOp = (DissolveCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

ModulateCompositeOp = (DisplaceCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

ThresholdCompositeOp = (ModulateCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

NoCompositeOp = (ThresholdCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

DarkenCompositeOp = (NoCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

LightenCompositeOp = (DarkenCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

HueCompositeOp = (LightenCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

SaturateCompositeOp = (HueCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

ColorizeCompositeOp = (SaturateCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

LuminizeCompositeOp = (ColorizeCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

ScreenCompositeOp = (LuminizeCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

OverlayCompositeOp = (ScreenCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

CopyCyanCompositeOp = (OverlayCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

CopyMagentaCompositeOp = (CopyCyanCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

CopyYellowCompositeOp = (CopyMagentaCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

CopyBlackCompositeOp = (CopyYellowCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

DivideCompositeOp = (CopyBlackCompositeOp + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

CompositeOperator = enum_anon_14 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 139

enum_anon_15 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

UndefinedCompression = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

NoCompression = (UndefinedCompression + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

BZipCompression = (NoCompression + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

FaxCompression = (BZipCompression + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

Group4Compression = (FaxCompression + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

JPEGCompression = (Group4Compression + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

LosslessJPEGCompression = (JPEGCompression + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

LZWCompression = (LosslessJPEGCompression + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

RLECompression = (LZWCompression + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

ZipCompression = (RLECompression + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

CompressionType = enum_anon_15 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 153

enum_anon_16 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 161

UndefinedDispose = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 161

NoneDispose = (UndefinedDispose + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 161

BackgroundDispose = (NoneDispose + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 161

PreviousDispose = (BackgroundDispose + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 161

DisposeType = enum_anon_16 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 161

enum_anon_17 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 169

UndefinedEndian = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 169

LSBEndian = (UndefinedEndian + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 169

MSBEndian = (LSBEndian + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 169

NativeEndian = (MSBEndian + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 169

EndianType = enum_anon_17 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 169

enum_anon_18 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

UndefinedFilter = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

PointFilter = (UndefinedFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

BoxFilter = (PointFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

TriangleFilter = (BoxFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

HermiteFilter = (TriangleFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

HanningFilter = (HermiteFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

HammingFilter = (HanningFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

BlackmanFilter = (HammingFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

GaussianFilter = (BlackmanFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

QuadraticFilter = (GaussianFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

CubicFilter = (QuadraticFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

CatromFilter = (CubicFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

MitchellFilter = (CatromFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

LanczosFilter = (MitchellFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

BesselFilter = (LanczosFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

SincFilter = (BesselFilter + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

FilterTypes = enum_anon_18 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 189

enum_anon_19 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

NoValue = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

XValue = 1 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

YValue = 2 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

WidthValue = 4 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

HeightValue = 8 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

AllValues = 15 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

XNegative = 16 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

YNegative = 32 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

PercentValue = 4096 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

AspectValue = 8192 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

LessValue = 16384 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

GreaterValue = 32768 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

AreaValue = 65536 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

MinimumValue = 131072 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

GeometryFlags = enum_anon_19 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 215

enum_anon_20 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

ForgetGravity = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

NorthWestGravity = (ForgetGravity + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

NorthGravity = (NorthWestGravity + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

NorthEastGravity = (NorthGravity + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

WestGravity = (NorthEastGravity + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

CenterGravity = (WestGravity + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

EastGravity = (CenterGravity + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

SouthWestGravity = (EastGravity + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

SouthGravity = (SouthWestGravity + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

SouthEastGravity = (SouthGravity + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

StaticGravity = (SouthEastGravity + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

GravityType = enum_anon_20 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 241

enum_anon_21 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

UndefinedType = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

BilevelType = (UndefinedType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

GrayscaleType = (BilevelType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

GrayscaleMatteType = (GrayscaleType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

PaletteType = (GrayscaleMatteType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

PaletteMatteType = (PaletteType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

TrueColorType = (PaletteMatteType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

TrueColorMatteType = (TrueColorType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

ColorSeparationType = (TrueColorMatteType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

ColorSeparationMatteType = (ColorSeparationType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

OptimizeType = (ColorSeparationMatteType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

ImageType = enum_anon_21 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 256

enum_anon_22 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 265

UndefinedInterlace = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 265

NoInterlace = (UndefinedInterlace + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 265

LineInterlace = (NoInterlace + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 265

PlaneInterlace = (LineInterlace + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 265

PartitionInterlace = (PlaneInterlace + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 265

InterlaceType = enum_anon_22 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 265

enum_anon_23 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 273

UndefinedMode = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 273

FrameMode = (UndefinedMode + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 273

UnframeMode = (FrameMode + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 273

ConcatenateMode = (UnframeMode + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 273

MontageMode = enum_anon_23 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 273

enum_anon_24 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 283

UniformNoise = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 283

GaussianNoise = (UniformNoise + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 283

MultiplicativeGaussianNoise = (GaussianNoise + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 283

ImpulseNoise = (MultiplicativeGaussianNoise + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 283

LaplacianNoise = (ImpulseNoise + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 283

PoissonNoise = (LaplacianNoise + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 283

NoiseType = enum_anon_24 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 283

enum_anon_25 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 299

UndefinedOrientation = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 299

TopLeftOrientation = (UndefinedOrientation + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 299

TopRightOrientation = (TopLeftOrientation + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 299

BottomRightOrientation = (TopRightOrientation + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 299

BottomLeftOrientation = (BottomRightOrientation + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 299

LeftTopOrientation = (BottomLeftOrientation + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 299

RightTopOrientation = (LeftTopOrientation + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 299

RightBottomOrientation = (RightTopOrientation + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 299

LeftBottomOrientation = (RightBottomOrientation + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 299

OrientationType = enum_anon_25 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 299

enum_anon_26 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

UndefinedPreview = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

RotatePreview = (UndefinedPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

ShearPreview = (RotatePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

RollPreview = (ShearPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

HuePreview = (RollPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

SaturationPreview = (HuePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

BrightnessPreview = (SaturationPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

GammaPreview = (BrightnessPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

SpiffPreview = (GammaPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

DullPreview = (SpiffPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

GrayscalePreview = (DullPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

QuantizePreview = (GrayscalePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

DespecklePreview = (QuantizePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

ReduceNoisePreview = (DespecklePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

AddNoisePreview = (ReduceNoisePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

SharpenPreview = (AddNoisePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

BlurPreview = (SharpenPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

ThresholdPreview = (BlurPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

EdgeDetectPreview = (ThresholdPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

SpreadPreview = (EdgeDetectPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

SolarizePreview = (SpreadPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

ShadePreview = (SolarizePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

RaisePreview = (ShadePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

SegmentPreview = (RaisePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

SwirlPreview = (SegmentPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

ImplodePreview = (SwirlPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

WavePreview = (ImplodePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

OilPaintPreview = (WavePreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

CharcoalDrawingPreview = (OilPaintPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

JPEGPreview = (CharcoalDrawingPreview + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

PreviewType = enum_anon_26 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 333

enum_anon_27 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 342

UndefinedIntent = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 342

SaturationIntent = (UndefinedIntent + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 342

PerceptualIntent = (SaturationIntent + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 342

AbsoluteIntent = (PerceptualIntent + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 342

RelativeIntent = (AbsoluteIntent + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 342

RenderingIntent = enum_anon_27 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 342

enum_anon_28 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 349

UndefinedResolution = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 349

PixelsPerInchResolution = (UndefinedResolution + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 349

PixelsPerCentimeterResolution = (PixelsPerInchResolution + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 349

ResolutionType = enum_anon_28 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 349

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 363
class struct__AffineMatrix(Structure):
    pass

struct__AffineMatrix.__slots__ = [
    'sx',
    'rx',
    'ry',
    'sy',
    'tx',
    'ty',
]
struct__AffineMatrix._fields_ = [
    ('sx', c_double),
    ('rx', c_double),
    ('ry', c_double),
    ('sy', c_double),
    ('tx', c_double),
    ('ty', c_double),
]

AffineMatrix = struct__AffineMatrix # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 363

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 371
class struct__PrimaryInfo(Structure):
    pass

struct__PrimaryInfo.__slots__ = [
    'x',
    'y',
    'z',
]
struct__PrimaryInfo._fields_ = [
    ('x', c_double),
    ('y', c_double),
    ('z', c_double),
]

PrimaryInfo = struct__PrimaryInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 371

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 380
class struct__ChromaticityInfo(Structure):
    pass

struct__ChromaticityInfo.__slots__ = [
    'red_primary',
    'green_primary',
    'blue_primary',
    'white_point',
]
struct__ChromaticityInfo._fields_ = [
    ('red_primary', PrimaryInfo),
    ('green_primary', PrimaryInfo),
    ('blue_primary', PrimaryInfo),
    ('white_point', PrimaryInfo),
]

ChromaticityInfo = struct__ChromaticityInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 380

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 438
class struct__PixelPacket(Structure):
    pass

struct__PixelPacket.__slots__ = [
    'blue',
    'green',
    'red',
    'opacity',
]
struct__PixelPacket._fields_ = [
    ('blue', Quantum),
    ('green', Quantum),
    ('red', Quantum),
    ('opacity', Quantum),
]

PixelPacket = struct__PixelPacket # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 438

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 447
class struct__DoublePixelPacket(Structure):
    pass

struct__DoublePixelPacket.__slots__ = [
    'red',
    'green',
    'blue',
    'opacity',
]
struct__DoublePixelPacket._fields_ = [
    ('red', c_double),
    ('green', c_double),
    ('blue', c_double),
    ('opacity', c_double),
]

DoublePixelPacket = struct__DoublePixelPacket # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 447

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 459
class struct__ErrorInfo(Structure):
    pass

struct__ErrorInfo.__slots__ = [
    'mean_error_per_pixel',
    'normalized_mean_error',
    'normalized_maximum_error',
]
struct__ErrorInfo._fields_ = [
    ('mean_error_per_pixel', c_double),
    ('normalized_mean_error', c_double),
    ('normalized_maximum_error', c_double),
]

ErrorInfo = struct__ErrorInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 459

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 472
class struct__FrameInfo(Structure):
    pass

struct__FrameInfo.__slots__ = [
    'width',
    'height',
    'x',
    'y',
    'inner_bevel',
    'outer_bevel',
]
struct__FrameInfo._fields_ = [
    ('width', c_ulong),
    ('height', c_ulong),
    ('x', c_long),
    ('y', c_long),
    ('inner_bevel', c_long),
    ('outer_bevel', c_long),
]

FrameInfo = struct__FrameInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 472

IndexPacket = Quantum # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 474

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 483
class struct__LongPixelPacket(Structure):
    pass

struct__LongPixelPacket.__slots__ = [
    'red',
    'green',
    'blue',
    'opacity',
]
struct__LongPixelPacket._fields_ = [
    ('red', c_ulong),
    ('green', c_ulong),
    ('blue', c_ulong),
    ('opacity', c_ulong),
]

LongPixelPacket = struct__LongPixelPacket # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 483

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 519
class struct__MontageInfo(Structure):
    pass

struct__MontageInfo.__slots__ = [
    'geometry',
    'tile',
    'title',
    'frame',
    'texture',
    'font',
    'pointsize',
    'border_width',
    'shadow',
    'fill',
    'stroke',
    'background_color',
    'border_color',
    'matte_color',
    'gravity',
    'filename',
    'signature',
]
struct__MontageInfo._fields_ = [
    ('geometry', String),
    ('tile', String),
    ('title', String),
    ('frame', String),
    ('texture', String),
    ('font', String),
    ('pointsize', c_double),
    ('border_width', c_ulong),
    ('shadow', c_uint),
    ('fill', PixelPacket),
    ('stroke', PixelPacket),
    ('background_color', PixelPacket),
    ('border_color', PixelPacket),
    ('matte_color', PixelPacket),
    ('gravity', GravityType),
    ('filename', c_char * 2053),
    ('signature', c_ulong),
]

MontageInfo = struct__MontageInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 519

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 531
class struct__ProfileInfo(Structure):
    pass

struct__ProfileInfo.__slots__ = [
    'length',
    'name',
    'info',
]
struct__ProfileInfo._fields_ = [
    ('length', c_size_t),
    ('name', String),
    ('info', POINTER(c_ubyte)),
]

ProfileInfo = struct__ProfileInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 531

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 542
class struct__RectangleInfo(Structure):
    pass

struct__RectangleInfo.__slots__ = [
    'width',
    'height',
    'x',
    'y',
]
struct__RectangleInfo._fields_ = [
    ('width', c_ulong),
    ('height', c_ulong),
    ('x', c_long),
    ('y', c_long),
]

RectangleInfo = struct__RectangleInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 542

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 551
class struct__SegmentInfo(Structure):
    pass

struct__SegmentInfo.__slots__ = [
    'x1',
    'y1',
    'x2',
    'y2',
]
struct__SegmentInfo._fields_ = [
    ('x1', c_double),
    ('y1', c_double),
    ('x2', c_double),
    ('y2', c_double),
]

SegmentInfo = struct__SegmentInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 551

struct__Image.__slots__ = [
    'storage_class',
    'colorspace',
    'compression',
    'dither',
    'matte',
    'columns',
    'rows',
    'colors',
    'depth',
    'colormap',
    'background_color',
    'border_color',
    'matte_color',
    'gamma',
    'chromaticity',
    'orientation',
    'rendering_intent',
    'units',
    'montage',
    'directory',
    'geometry',
    'offset',
    'x_resolution',
    'y_resolution',
    'page',
    'tile_info',
    'blur',
    'fuzz',
    'filter',
    'interlace',
    'endian',
    'gravity',
    'compose',
    'dispose',
    'scene',
    'delay',
    'iterations',
    'total_colors',
    'start_loop',
    'error',
    'timer',
    'client_data',
    'filename',
    'magick_filename',
    'magick',
    'magick_columns',
    'magick_rows',
    'exception',
    'previous',
    'next',
    'profiles',
    'is_monochrome',
    'is_grayscale',
    'taint',
    'clip_mask',
    'ping',
    'cache',
    'default_views',
    'attributes',
    'ascii85',
    'blob',
    'reference_count',
    'semaphore',
    'logging',
    'list',
    'signature',
]
struct__Image._fields_ = [
    ('storage_class', ClassType),
    ('colorspace', ColorspaceType),
    ('compression', CompressionType),
    ('dither', c_uint),
    ('matte', c_uint),
    ('columns', c_ulong),
    ('rows', c_ulong),
    ('colors', c_uint),
    ('depth', c_uint),
    ('colormap', POINTER(PixelPacket)),
    ('background_color', PixelPacket),
    ('border_color', PixelPacket),
    ('matte_color', PixelPacket),
    ('gamma', c_double),
    ('chromaticity', ChromaticityInfo),
    ('orientation', OrientationType),
    ('rendering_intent', RenderingIntent),
    ('units', ResolutionType),
    ('montage', String),
    ('directory', String),
    ('geometry', String),
    ('offset', c_long),
    ('x_resolution', c_double),
    ('y_resolution', c_double),
    ('page', RectangleInfo),
    ('tile_info', RectangleInfo),
    ('blur', c_double),
    ('fuzz', c_double),
    ('filter', FilterTypes),
    ('interlace', InterlaceType),
    ('endian', EndianType),
    ('gravity', GravityType),
    ('compose', CompositeOperator),
    ('dispose', DisposeType),
    ('scene', c_ulong),
    ('delay', c_ulong),
    ('iterations', c_ulong),
    ('total_colors', c_ulong),
    ('start_loop', c_long),
    ('error', ErrorInfo),
    ('timer', TimerInfo),
    ('client_data', POINTER(None)),
    ('filename', c_char * 2053),
    ('magick_filename', c_char * 2053),
    ('magick', c_char * 2053),
    ('magick_columns', c_ulong),
    ('magick_rows', c_ulong),
    ('exception', ExceptionInfo),
    ('previous', POINTER(struct__Image)),
    ('next', POINTER(struct__Image)),
    ('profiles', POINTER(None)),
    ('is_monochrome', c_uint),
    ('is_grayscale', c_uint),
    ('taint', c_uint),
    ('clip_mask', POINTER(struct__Image)),
    ('ping', c_uint),
    ('cache', _CacheInfoPtr_),
    ('default_views', _ThreadViewSetPtr_),
    ('attributes', _ImageAttributePtr_),
    ('ascii85', _Ascii85InfoPtr_),
    ('blob', _BlobInfoPtr_),
    ('reference_count', c_long),
    ('semaphore', _SemaphoreInfoPtr_),
    ('logging', c_uint),
    ('list', POINTER(struct__Image)),
    ('signature', c_ulong),
]

Image = struct__Image # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 760

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 880
class struct__ImageInfo(Structure):
    pass

struct__ImageInfo.__slots__ = [
    'compression',
    'temporary',
    'adjoin',
    'antialias',
    'subimage',
    'subrange',
    'depth',
    'size',
    'tile',
    'page',
    'interlace',
    'endian',
    'units',
    'quality',
    'sampling_factor',
    'server_name',
    'font',
    'texture',
    'density',
    'pointsize',
    'fuzz',
    'pen',
    'background_color',
    'border_color',
    'matte_color',
    'dither',
    'monochrome',
    'progress',
    'colorspace',
    'type',
    'group',
    'verbose',
    'view',
    'authenticate',
    'client_data',
    'file',
    'magick',
    'filename',
    'cache',
    'definitions',
    'attributes',
    'ping',
    'preview_type',
    'affirm',
    'blob',
    'length',
    'unique',
    'zero',
    'signature',
]
struct__ImageInfo._fields_ = [
    ('compression', CompressionType),
    ('temporary', c_uint),
    ('adjoin', c_uint),
    ('antialias', c_uint),
    ('subimage', c_ulong),
    ('subrange', c_ulong),
    ('depth', c_ulong),
    ('size', String),
    ('tile', String),
    ('page', String),
    ('interlace', InterlaceType),
    ('endian', EndianType),
    ('units', ResolutionType),
    ('quality', c_ulong),
    ('sampling_factor', String),
    ('server_name', String),
    ('font', String),
    ('texture', String),
    ('density', String),
    ('pointsize', c_double),
    ('fuzz', c_double),
    ('pen', PixelPacket),
    ('background_color', PixelPacket),
    ('border_color', PixelPacket),
    ('matte_color', PixelPacket),
    ('dither', c_uint),
    ('monochrome', c_uint),
    ('progress', c_uint),
    ('colorspace', ColorspaceType),
    ('type', ImageType),
    ('group', c_long),
    ('verbose', c_uint),
    ('view', String),
    ('authenticate', String),
    ('client_data', POINTER(None)),
    ('file', POINTER(FILE)),
    ('magick', c_char * 2053),
    ('filename', c_char * 2053),
    ('cache', _CacheInfoPtr_),
    ('definitions', POINTER(None)),
    ('attributes', POINTER(Image)),
    ('ping', c_uint),
    ('preview_type', PreviewType),
    ('affirm', c_uint),
    ('blob', _BlobInfoPtr_),
    ('length', c_size_t),
    ('unique', c_char * 2053),
    ('zero', c_char * 2053),
    ('signature', c_ulong),
]

ImageInfo = struct__ImageInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 880

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 887
if hasattr(_libs['GraphicsMagick'], 'CatchImageException'):
    CatchImageException = _libs['GraphicsMagick'].CatchImageException
    CatchImageException.argtypes = [POINTER(Image)]
    CatchImageException.restype = ExceptionType

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 890
if hasattr(_libs['GraphicsMagick'], 'AllocateImage'):
    AllocateImage = _libs['GraphicsMagick'].AllocateImage
    AllocateImage.argtypes = [POINTER(ImageInfo)]
    AllocateImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 890
if hasattr(_libs['GraphicsMagick'], 'AppendImages'):
    AppendImages = _libs['GraphicsMagick'].AppendImages
    AppendImages.argtypes = [POINTER(Image), c_uint, POINTER(ExceptionInfo)]
    AppendImages.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 890
if hasattr(_libs['GraphicsMagick'], 'CloneImage'):
    CloneImage = _libs['GraphicsMagick'].CloneImage
    CloneImage.argtypes = [POINTER(Image), c_ulong, c_ulong, c_uint, POINTER(ExceptionInfo)]
    CloneImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 890
if hasattr(_libs['GraphicsMagick'], 'GetImageClipMask'):
    GetImageClipMask = _libs['GraphicsMagick'].GetImageClipMask
    GetImageClipMask.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    GetImageClipMask.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 890
if hasattr(_libs['GraphicsMagick'], 'ReferenceImage'):
    ReferenceImage = _libs['GraphicsMagick'].ReferenceImage
    ReferenceImage.argtypes = [POINTER(Image)]
    ReferenceImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 898
if hasattr(_libs['GraphicsMagick'], 'CloneImageInfo'):
    CloneImageInfo = _libs['GraphicsMagick'].CloneImageInfo
    CloneImageInfo.argtypes = [POINTER(ImageInfo)]
    CloneImageInfo.restype = POINTER(ImageInfo)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 901
if hasattr(_libs['GraphicsMagick'], 'AccessDefinition'):
    AccessDefinition = _libs['GraphicsMagick'].AccessDefinition
    AccessDefinition.argtypes = [POINTER(ImageInfo), String, String]
    if sizeof(c_int) == sizeof(c_void_p):
        AccessDefinition.restype = ReturnString
    else:
        AccessDefinition.restype = String
        AccessDefinition.errcheck = ReturnString

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 905
if hasattr(_libs['GraphicsMagick'], 'GetImageGeometry'):
    GetImageGeometry = _libs['GraphicsMagick'].GetImageGeometry
    GetImageGeometry.argtypes = [POINTER(Image), String, c_uint, POINTER(RectangleInfo)]
    GetImageGeometry.restype = c_int

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 910
if hasattr(_libs['GraphicsMagick'], 'IsTaintImage'):
    IsTaintImage = _libs['GraphicsMagick'].IsTaintImage
    IsTaintImage.argtypes = [POINTER(Image)]
    IsTaintImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 910
if hasattr(_libs['GraphicsMagick'], 'IsSubimage'):
    IsSubimage = _libs['GraphicsMagick'].IsSubimage
    IsSubimage.argtypes = [String, c_uint]
    IsSubimage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'AddDefinitions'):
    AddDefinitions = _libs['GraphicsMagick'].AddDefinitions
    AddDefinitions.argtypes = [POINTER(ImageInfo), String, POINTER(ExceptionInfo)]
    AddDefinitions.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'AnimateImages'):
    AnimateImages = _libs['GraphicsMagick'].AnimateImages
    AnimateImages.argtypes = [POINTER(ImageInfo), POINTER(Image)]
    AnimateImages.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'ClipImage'):
    ClipImage = _libs['GraphicsMagick'].ClipImage
    ClipImage.argtypes = [POINTER(Image)]
    ClipImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'ClipPathImage'):
    ClipPathImage = _libs['GraphicsMagick'].ClipPathImage
    ClipPathImage.argtypes = [POINTER(Image), String, c_uint]
    ClipPathImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'DisplayImages'):
    DisplayImages = _libs['GraphicsMagick'].DisplayImages
    DisplayImages.argtypes = [POINTER(ImageInfo), POINTER(Image)]
    DisplayImages.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'RemoveDefinitions'):
    RemoveDefinitions = _libs['GraphicsMagick'].RemoveDefinitions
    RemoveDefinitions.argtypes = [POINTER(ImageInfo), String]
    RemoveDefinitions.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'SetImage'):
    SetImage = _libs['GraphicsMagick'].SetImage
    SetImage.argtypes = [POINTER(Image), Quantum]
    SetImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'SetImageClipMask'):
    SetImageClipMask = _libs['GraphicsMagick'].SetImageClipMask
    SetImageClipMask.argtypes = [POINTER(Image), POINTER(Image)]
    SetImageClipMask.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'SetImageDepth'):
    SetImageDepth = _libs['GraphicsMagick'].SetImageDepth
    SetImageDepth.argtypes = [POINTER(Image), c_ulong]
    SetImageDepth.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'SetImageInfo'):
    SetImageInfo = _libs['GraphicsMagick'].SetImageInfo
    SetImageInfo.argtypes = [POINTER(ImageInfo), c_uint, POINTER(ExceptionInfo)]
    SetImageInfo.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'SetImageType'):
    SetImageType = _libs['GraphicsMagick'].SetImageType
    SetImageType.argtypes = [POINTER(Image), ImageType]
    SetImageType.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 915
if hasattr(_libs['GraphicsMagick'], 'SyncImage'):
    SyncImage = _libs['GraphicsMagick'].SyncImage
    SyncImage.argtypes = [POINTER(Image)]
    SyncImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 930
if hasattr(_libs['GraphicsMagick'], 'AllocateNextImage'):
    AllocateNextImage = _libs['GraphicsMagick'].AllocateNextImage
    AllocateNextImage.argtypes = [POINTER(ImageInfo), POINTER(Image)]
    AllocateNextImage.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 930
if hasattr(_libs['GraphicsMagick'], 'DestroyImage'):
    DestroyImage = _libs['GraphicsMagick'].DestroyImage
    DestroyImage.argtypes = [POINTER(Image)]
    DestroyImage.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 930
if hasattr(_libs['GraphicsMagick'], 'DestroyImageInfo'):
    DestroyImageInfo = _libs['GraphicsMagick'].DestroyImageInfo
    DestroyImageInfo.argtypes = [POINTER(ImageInfo)]
    DestroyImageInfo.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 930
if hasattr(_libs['GraphicsMagick'], 'GetImageException'):
    GetImageException = _libs['GraphicsMagick'].GetImageException
    GetImageException.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    GetImageException.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 930
if hasattr(_libs['GraphicsMagick'], 'GetImageInfo'):
    GetImageInfo = _libs['GraphicsMagick'].GetImageInfo
    GetImageInfo.argtypes = [POINTER(ImageInfo)]
    GetImageInfo.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 930
if hasattr(_libs['GraphicsMagick'], 'ModifyImage'):
    ModifyImage = _libs['GraphicsMagick'].ModifyImage
    ModifyImage.argtypes = [POINTER(POINTER(Image)), POINTER(ExceptionInfo)]
    ModifyImage.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 930
if hasattr(_libs['GraphicsMagick'], 'SetImageOpacity'):
    SetImageOpacity = _libs['GraphicsMagick'].SetImageOpacity
    SetImageOpacity.argtypes = [POINTER(Image), c_uint]
    SetImageOpacity.restype = None

DecoderHandler = CFUNCTYPE(UNCHECKED(POINTER(Image)), POINTER(ImageInfo), POINTER(ExceptionInfo)) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 20

EncoderHandler = CFUNCTYPE(UNCHECKED(c_uint), POINTER(ImageInfo), POINTER(Image)) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 23

MagickHandler = CFUNCTYPE(UNCHECKED(c_uint), POINTER(c_ubyte), c_size_t) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 23

enum_anon_29 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 34

UnstableCoderClass = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 34

StableCoderClass = (UnstableCoderClass + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 34

PrimaryCoderClass = (StableCoderClass + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 34

CoderClass = enum_anon_29 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 34

enum_anon_30 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 44

HintExtensionTreatment = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 44

ObeyExtensionTreatment = (HintExtensionTreatment + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 44

IgnoreExtensionTreatment = (ObeyExtensionTreatment + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 44

ExtensionTreatment = enum_anon_30 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 44

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 46
class struct__MagickInfo(Structure):
    pass

struct__MagickInfo.__slots__ = [
    'next',
    'previous',
    'name',
    'description',
    'note',
    'version',
    'module',
    'decoder',
    'encoder',
    'magick',
    'client_data',
    'adjoin',
    'raw',
    'stealth',
    'seekable_stream',
    'blob_support',
    'thread_support',
    'coder_class',
    'extension_treatment',
    'signature',
]
struct__MagickInfo._fields_ = [
    ('next', POINTER(struct__MagickInfo)),
    ('previous', POINTER(struct__MagickInfo)),
    ('name', String),
    ('description', String),
    ('note', String),
    ('version', String),
    ('module', String),
    ('decoder', DecoderHandler),
    ('encoder', EncoderHandler),
    ('magick', MagickHandler),
    ('client_data', POINTER(None)),
    ('adjoin', c_uint),
    ('raw', c_uint),
    ('stealth', c_uint),
    ('seekable_stream', c_uint),
    ('blob_support', c_uint),
    ('thread_support', c_uint),
    ('coder_class', CoderClass),
    ('extension_treatment', ExtensionTreatment),
    ('signature', c_ulong),
]

MagickInfo = struct__MagickInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 95

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 101
if hasattr(_libs['GraphicsMagick'], 'MagickToMime'):
    MagickToMime = _libs['GraphicsMagick'].MagickToMime
    MagickToMime.argtypes = [String]
    if sizeof(c_int) == sizeof(c_void_p):
        MagickToMime.restype = ReturnString
    else:
        MagickToMime.restype = String
        MagickToMime.errcheck = ReturnString

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 104
if hasattr(_libs['GraphicsMagick'], 'GetImageMagick'):
    GetImageMagick = _libs['GraphicsMagick'].GetImageMagick
    GetImageMagick.argtypes = [POINTER(c_ubyte), c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        GetImageMagick.restype = ReturnString
    else:
        GetImageMagick.restype = String
        GetImageMagick.errcheck = ReturnString

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 107
if hasattr(_libs['GraphicsMagick'], 'IsMagickConflict'):
    IsMagickConflict = _libs['GraphicsMagick'].IsMagickConflict
    IsMagickConflict.argtypes = [String]
    IsMagickConflict.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 110
if hasattr(_libs['GraphicsMagick'], 'ListModuleMap'):
    ListModuleMap = _libs['GraphicsMagick'].ListModuleMap
    ListModuleMap.argtypes = [POINTER(FILE), POINTER(ExceptionInfo)]
    ListModuleMap.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 110
if hasattr(_libs['GraphicsMagick'], 'ListMagickInfo'):
    ListMagickInfo = _libs['GraphicsMagick'].ListMagickInfo
    ListMagickInfo.argtypes = [POINTER(FILE), POINTER(ExceptionInfo)]
    ListMagickInfo.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 110
if hasattr(_libs['GraphicsMagick'], 'UnregisterMagickInfo'):
    UnregisterMagickInfo = _libs['GraphicsMagick'].UnregisterMagickInfo
    UnregisterMagickInfo.argtypes = [String]
    UnregisterMagickInfo.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 115
if hasattr(_libs['GraphicsMagick'], 'DestroyMagick'):
    DestroyMagick = _libs['GraphicsMagick'].DestroyMagick
    DestroyMagick.argtypes = []
    DestroyMagick.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 115
if hasattr(_libs['GraphicsMagick'], 'InitializeMagick'):
    InitializeMagick = _libs['GraphicsMagick'].InitializeMagick
    InitializeMagick.argtypes = [String]
    InitializeMagick.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 119
if hasattr(_libs['GraphicsMagick'], 'GetMagickInfo'):
    GetMagickInfo = _libs['GraphicsMagick'].GetMagickInfo
    GetMagickInfo.argtypes = [String, POINTER(ExceptionInfo)]
    GetMagickInfo.restype = POINTER(MagickInfo)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 122
if hasattr(_libs['GraphicsMagick'], 'GetMagickInfoArray'):
    GetMagickInfoArray = _libs['GraphicsMagick'].GetMagickInfoArray
    GetMagickInfoArray.argtypes = [POINTER(ExceptionInfo)]
    GetMagickInfoArray.restype = POINTER(POINTER(MagickInfo))

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 125
if hasattr(_libs['GraphicsMagick'], 'RegisterMagickInfo'):
    RegisterMagickInfo = _libs['GraphicsMagick'].RegisterMagickInfo
    RegisterMagickInfo.argtypes = [POINTER(MagickInfo)]
    RegisterMagickInfo.restype = POINTER(MagickInfo)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 125
if hasattr(_libs['GraphicsMagick'], 'SetMagickInfo'):
    SetMagickInfo = _libs['GraphicsMagick'].SetMagickInfo
    SetMagickInfo.argtypes = [String]
    SetMagickInfo.restype = POINTER(MagickInfo)

enum_anon_31 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

UndefinedQuantum = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

IndexQuantum = (UndefinedQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

GrayQuantum = (IndexQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

IndexAlphaQuantum = (GrayQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

GrayAlphaQuantum = (IndexAlphaQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

RedQuantum = (GrayAlphaQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

CyanQuantum = (RedQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

GreenQuantum = (CyanQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

YellowQuantum = (GreenQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

BlueQuantum = (YellowQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

MagentaQuantum = (BlueQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

AlphaQuantum = (MagentaQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

BlackQuantum = (AlphaQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

RGBQuantum = (BlackQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

RGBAQuantum = (RGBQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

CMYKQuantum = (RGBAQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

CMYKAQuantum = (CMYKQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

CIEYQuantum = (CMYKAQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

CIEXYZQuantum = (CIEYQuantum + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

QuantumType = enum_anon_31 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 46

enum_anon_32 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 56

UndefinedQuantumSampleType = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 56

UnsignedQuantumSampleType = (UndefinedQuantumSampleType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 56

FloatQuantumSampleType = (UnsignedQuantumSampleType + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 56

QuantumSampleType = enum_anon_32 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 56

enum_anon_33 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 69

CharPixel = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 69

ShortPixel = (CharPixel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 69

IntegerPixel = (ShortPixel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 69

LongPixel = (IntegerPixel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 69

FloatPixel = (LongPixel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 69

DoublePixel = (FloatPixel + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 69

StorageType = enum_anon_33 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 69

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 97
class struct__ExportPixelAreaOptions(Structure):
    pass

struct__ExportPixelAreaOptions.__slots__ = [
    'sample_type',
    'double_minvalue',
    'double_maxvalue',
    'grayscale_miniswhite',
    'pad_bytes',
    'pad_value',
    'endian',
    'signature',
]
struct__ExportPixelAreaOptions._fields_ = [
    ('sample_type', QuantumSampleType),
    ('double_minvalue', c_double),
    ('double_maxvalue', c_double),
    ('grayscale_miniswhite', c_uint),
    ('pad_bytes', c_ulong),
    ('pad_value', c_ubyte),
    ('endian', EndianType),
    ('signature', c_ulong),
]

ExportPixelAreaOptions = struct__ExportPixelAreaOptions # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 97

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 107
class struct__ExportPixelAreaInfo(Structure):
    pass

struct__ExportPixelAreaInfo.__slots__ = [
    'bytes_exported',
]
struct__ExportPixelAreaInfo._fields_ = [
    ('bytes_exported', c_size_t),
]

ExportPixelAreaInfo = struct__ExportPixelAreaInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 107

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 129
class struct__ImportPixelAreaOptions(Structure):
    pass

struct__ImportPixelAreaOptions.__slots__ = [
    'sample_type',
    'double_minvalue',
    'double_maxvalue',
    'grayscale_miniswhite',
    'endian',
    'signature',
]
struct__ImportPixelAreaOptions._fields_ = [
    ('sample_type', QuantumSampleType),
    ('double_minvalue', c_double),
    ('double_maxvalue', c_double),
    ('grayscale_miniswhite', c_uint),
    ('endian', EndianType),
    ('signature', c_ulong),
]

ImportPixelAreaOptions = struct__ImportPixelAreaOptions # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 129

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 139
class struct__ImportPixelAreaInfo(Structure):
    pass

struct__ImportPixelAreaInfo.__slots__ = [
    'bytes_imported',
]
struct__ImportPixelAreaInfo._fields_ = [
    ('bytes_imported', c_size_t),
]

ImportPixelAreaInfo = struct__ImportPixelAreaInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 139

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 142
if hasattr(_libs['GraphicsMagick'], 'StorageTypeToString'):
    StorageTypeToString = _libs['GraphicsMagick'].StorageTypeToString
    StorageTypeToString.argtypes = [StorageType]
    if sizeof(c_int) == sizeof(c_void_p):
        StorageTypeToString.restype = ReturnString
    else:
        StorageTypeToString.restype = String
        StorageTypeToString.errcheck = ReturnString

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 142
if hasattr(_libs['GraphicsMagick'], 'QuantumSampleTypeToString'):
    QuantumSampleTypeToString = _libs['GraphicsMagick'].QuantumSampleTypeToString
    QuantumSampleTypeToString.argtypes = [QuantumSampleType]
    if sizeof(c_int) == sizeof(c_void_p):
        QuantumSampleTypeToString.restype = ReturnString
    else:
        QuantumSampleTypeToString.restype = String
        QuantumSampleTypeToString.errcheck = ReturnString

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 142
if hasattr(_libs['GraphicsMagick'], 'QuantumTypeToString'):
    QuantumTypeToString = _libs['GraphicsMagick'].QuantumTypeToString
    QuantumTypeToString.argtypes = [QuantumType]
    if sizeof(c_int) == sizeof(c_void_p):
        QuantumTypeToString.restype = ReturnString
    else:
        QuantumTypeToString.restype = String
        QuantumTypeToString.errcheck = ReturnString

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 147
if hasattr(_libs['GraphicsMagick'], 'ConstituteImage'):
    ConstituteImage = _libs['GraphicsMagick'].ConstituteImage
    ConstituteImage.argtypes = [c_ulong, c_ulong, String, StorageType, POINTER(None), POINTER(ExceptionInfo)]
    ConstituteImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 147
if hasattr(_libs['GraphicsMagick'], 'ConstituteTextureImage'):
    ConstituteTextureImage = _libs['GraphicsMagick'].ConstituteTextureImage
    ConstituteTextureImage.argtypes = [c_ulong, c_ulong, POINTER(Image), POINTER(ExceptionInfo)]
    ConstituteTextureImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 147
if hasattr(_libs['GraphicsMagick'], 'PingImage'):
    PingImage = _libs['GraphicsMagick'].PingImage
    PingImage.argtypes = [POINTER(ImageInfo), POINTER(ExceptionInfo)]
    PingImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 147
if hasattr(_libs['GraphicsMagick'], 'ReadImage'):
    ReadImage = _libs['GraphicsMagick'].ReadImage
    ReadImage.argtypes = [POINTER(ImageInfo), POINTER(ExceptionInfo)]
    ReadImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 147
if hasattr(_libs['GraphicsMagick'], 'ReadInlineImage'):
    ReadInlineImage = _libs['GraphicsMagick'].ReadInlineImage
    ReadInlineImage.argtypes = [POINTER(ImageInfo), String, POINTER(ExceptionInfo)]
    ReadInlineImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 158
if hasattr(_libs['GraphicsMagick'], 'DispatchImage'):
    DispatchImage = _libs['GraphicsMagick'].DispatchImage
    DispatchImage.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong, String, StorageType, POINTER(None), POINTER(ExceptionInfo)]
    DispatchImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 158
if hasattr(_libs['GraphicsMagick'], 'ExportImagePixelArea'):
    ExportImagePixelArea = _libs['GraphicsMagick'].ExportImagePixelArea
    ExportImagePixelArea.argtypes = [POINTER(Image), QuantumType, c_uint, POINTER(c_ubyte), POINTER(ExportPixelAreaOptions), POINTER(ExportPixelAreaInfo)]
    ExportImagePixelArea.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 158
if hasattr(_libs['GraphicsMagick'], 'ExportViewPixelArea'):
    ExportViewPixelArea = _libs['GraphicsMagick'].ExportViewPixelArea
    ExportViewPixelArea.argtypes = [POINTER(ViewInfo), QuantumType, c_uint, POINTER(c_ubyte), POINTER(ExportPixelAreaOptions), POINTER(ExportPixelAreaInfo)]
    ExportViewPixelArea.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 169
if hasattr(_libs['GraphicsMagick'], 'ImportImagePixelArea'):
    ImportImagePixelArea = _libs['GraphicsMagick'].ImportImagePixelArea
    ImportImagePixelArea.argtypes = [POINTER(Image), QuantumType, c_uint, POINTER(c_ubyte), POINTER(ImportPixelAreaOptions), POINTER(ImportPixelAreaInfo)]
    ImportImagePixelArea.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 169
if hasattr(_libs['GraphicsMagick'], 'ImportViewPixelArea'):
    ImportViewPixelArea = _libs['GraphicsMagick'].ImportViewPixelArea
    ImportViewPixelArea.argtypes = [POINTER(ViewInfo), QuantumType, c_uint, POINTER(c_ubyte), POINTER(ImportPixelAreaOptions), POINTER(ImportPixelAreaInfo)]
    ImportViewPixelArea.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 169
if hasattr(_libs['GraphicsMagick'], 'WriteImage'):
    WriteImage = _libs['GraphicsMagick'].WriteImage
    WriteImage.argtypes = [POINTER(ImageInfo), POINTER(Image)]
    WriteImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 169
if hasattr(_libs['GraphicsMagick'], 'WriteImages'):
    WriteImages = _libs['GraphicsMagick'].WriteImages
    WriteImages.argtypes = [POINTER(ImageInfo), POINTER(Image), String, POINTER(ExceptionInfo)]
    WriteImages.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 180
if hasattr(_libs['GraphicsMagick'], 'ExportPixelAreaOptionsInit'):
    ExportPixelAreaOptionsInit = _libs['GraphicsMagick'].ExportPixelAreaOptionsInit
    ExportPixelAreaOptionsInit.argtypes = [POINTER(ExportPixelAreaOptions)]
    ExportPixelAreaOptionsInit.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 180
if hasattr(_libs['GraphicsMagick'], 'ImportPixelAreaOptionsInit'):
    ImportPixelAreaOptionsInit = _libs['GraphicsMagick'].ImportPixelAreaOptionsInit
    ImportPixelAreaOptionsInit.argtypes = [POINTER(ImportPixelAreaOptions)]
    ImportPixelAreaOptionsInit.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 184
if hasattr(_libs['GraphicsMagick'], 'MagickFindRawImageMinMax'):
    MagickFindRawImageMinMax = _libs['GraphicsMagick'].MagickFindRawImageMinMax
    MagickFindRawImageMinMax.argtypes = [POINTER(Image), EndianType, c_ulong, c_ulong, StorageType, c_uint, POINTER(None), POINTER(c_double), POINTER(c_double)]
    MagickFindRawImageMinMax.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/resize.h: 21
if hasattr(_libs['GraphicsMagick'], 'MagnifyImage'):
    MagnifyImage = _libs['GraphicsMagick'].MagnifyImage
    MagnifyImage.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    MagnifyImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/resize.h: 21
if hasattr(_libs['GraphicsMagick'], 'MinifyImage'):
    MinifyImage = _libs['GraphicsMagick'].MinifyImage
    MinifyImage.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    MinifyImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/resize.h: 21
if hasattr(_libs['GraphicsMagick'], 'ResizeImage'):
    ResizeImage = _libs['GraphicsMagick'].ResizeImage
    ResizeImage.argtypes = [POINTER(Image), c_ulong, c_ulong, FilterTypes, c_double, POINTER(ExceptionInfo)]
    ResizeImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/resize.h: 21
if hasattr(_libs['GraphicsMagick'], 'SampleImage'):
    SampleImage = _libs['GraphicsMagick'].SampleImage
    SampleImage.argtypes = [POINTER(Image), c_ulong, c_ulong, POINTER(ExceptionInfo)]
    SampleImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/resize.h: 21
if hasattr(_libs['GraphicsMagick'], 'ScaleImage'):
    ScaleImage = _libs['GraphicsMagick'].ScaleImage
    ScaleImage.argtypes = [POINTER(Image), c_ulong, c_ulong, POINTER(ExceptionInfo)]
    ScaleImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/resize.h: 21
if hasattr(_libs['GraphicsMagick'], 'ThumbnailImage'):
    ThumbnailImage = _libs['GraphicsMagick'].ThumbnailImage
    ThumbnailImage.argtypes = [POINTER(Image), c_ulong, c_ulong, POINTER(ExceptionInfo)]
    ThumbnailImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/resize.h: 21
if hasattr(_libs['GraphicsMagick'], 'ZoomImage'):
    ZoomImage = _libs['GraphicsMagick'].ZoomImage
    ZoomImage.argtypes = [POINTER(Image), c_ulong, c_ulong, POINTER(ExceptionInfo)]
    ZoomImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/delegate.h: 21
class struct__DelegateInfo(Structure):
    pass

struct__DelegateInfo.__slots__ = [
    'path',
    'decode',
    'encode',
    'commands',
    'mode',
    'stealth',
    'signature',
    'previous',
    'next',
]
struct__DelegateInfo._fields_ = [
    ('path', String),
    ('decode', String),
    ('encode', String),
    ('commands', String),
    ('mode', c_int),
    ('stealth', c_uint),
    ('signature', c_ulong),
    ('previous', POINTER(struct__DelegateInfo)),
    ('next', POINTER(struct__DelegateInfo)),
]

DelegateInfo = struct__DelegateInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/delegate.h: 42

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/delegate.h: 48
if hasattr(_libs['GraphicsMagick'], 'GetDelegateCommand'):
    GetDelegateCommand = _libs['GraphicsMagick'].GetDelegateCommand
    GetDelegateCommand.argtypes = [POINTER(ImageInfo), POINTER(Image), String, String, POINTER(ExceptionInfo)]
    if sizeof(c_int) == sizeof(c_void_p):
        GetDelegateCommand.restype = ReturnString
    else:
        GetDelegateCommand.restype = String
        GetDelegateCommand.errcheck = ReturnString

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/delegate.h: 53
if hasattr(_libs['GraphicsMagick'], 'GetDelegateInfo'):
    GetDelegateInfo = _libs['GraphicsMagick'].GetDelegateInfo
    GetDelegateInfo.argtypes = [String, String, POINTER(ExceptionInfo)]
    GetDelegateInfo.restype = POINTER(DelegateInfo)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/delegate.h: 53
if hasattr(_libs['GraphicsMagick'], 'GetPostscriptDelegateInfo'):
    GetPostscriptDelegateInfo = _libs['GraphicsMagick'].GetPostscriptDelegateInfo
    GetPostscriptDelegateInfo.argtypes = [POINTER(ImageInfo), POINTER(c_uint), POINTER(ExceptionInfo)]
    GetPostscriptDelegateInfo.restype = POINTER(DelegateInfo)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/delegate.h: 59
if hasattr(_libs['GraphicsMagick'], 'SetDelegateInfo'):
    SetDelegateInfo = _libs['GraphicsMagick'].SetDelegateInfo
    SetDelegateInfo.argtypes = [POINTER(DelegateInfo)]
    SetDelegateInfo.restype = POINTER(DelegateInfo)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/delegate.h: 62
if hasattr(_libs['GraphicsMagick'], 'InvokePostscriptDelegate'):
    InvokePostscriptDelegate = _libs['GraphicsMagick'].InvokePostscriptDelegate
    InvokePostscriptDelegate.argtypes = [c_uint, String, POINTER(ExceptionInfo)]
    InvokePostscriptDelegate.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/delegate.h: 62
if hasattr(_libs['GraphicsMagick'], 'InvokeDelegate'):
    InvokeDelegate = _libs['GraphicsMagick'].InvokeDelegate
    InvokeDelegate.argtypes = [POINTER(ImageInfo), POINTER(Image), String, String, POINTER(ExceptionInfo)]
    InvokeDelegate.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/delegate.h: 62
if hasattr(_libs['GraphicsMagick'], 'ListDelegateInfo'):
    ListDelegateInfo = _libs['GraphicsMagick'].ListDelegateInfo
    ListDelegateInfo.argtypes = [POINTER(FILE), POINTER(ExceptionInfo)]
    ListDelegateInfo.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'AdaptiveThresholdImage'):
    AdaptiveThresholdImage = _libs['GraphicsMagick'].AdaptiveThresholdImage
    AdaptiveThresholdImage.argtypes = [POINTER(Image), c_ulong, c_ulong, c_double, POINTER(ExceptionInfo)]
    AdaptiveThresholdImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'AddNoiseImage'):
    AddNoiseImage = _libs['GraphicsMagick'].AddNoiseImage
    AddNoiseImage.argtypes = [POINTER(Image), NoiseType, POINTER(ExceptionInfo)]
    AddNoiseImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'AddNoiseImageChannel'):
    AddNoiseImageChannel = _libs['GraphicsMagick'].AddNoiseImageChannel
    AddNoiseImageChannel.argtypes = [POINTER(Image), ChannelType, NoiseType, POINTER(ExceptionInfo)]
    AddNoiseImageChannel.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'BlurImage'):
    BlurImage = _libs['GraphicsMagick'].BlurImage
    BlurImage.argtypes = [POINTER(Image), c_double, c_double, POINTER(ExceptionInfo)]
    BlurImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'BlurImageChannel'):
    BlurImageChannel = _libs['GraphicsMagick'].BlurImageChannel
    BlurImageChannel.argtypes = [POINTER(Image), ChannelType, c_double, c_double, POINTER(ExceptionInfo)]
    BlurImageChannel.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'ConvolveImage'):
    ConvolveImage = _libs['GraphicsMagick'].ConvolveImage
    ConvolveImage.argtypes = [POINTER(Image), c_uint, POINTER(c_double), POINTER(ExceptionInfo)]
    ConvolveImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'DespeckleImage'):
    DespeckleImage = _libs['GraphicsMagick'].DespeckleImage
    DespeckleImage.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    DespeckleImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'EdgeImage'):
    EdgeImage = _libs['GraphicsMagick'].EdgeImage
    EdgeImage.argtypes = [POINTER(Image), c_double, POINTER(ExceptionInfo)]
    EdgeImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'EmbossImage'):
    EmbossImage = _libs['GraphicsMagick'].EmbossImage
    EmbossImage.argtypes = [POINTER(Image), c_double, c_double, POINTER(ExceptionInfo)]
    EmbossImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'EnhanceImage'):
    EnhanceImage = _libs['GraphicsMagick'].EnhanceImage
    EnhanceImage.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    EnhanceImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'GaussianBlurImage'):
    GaussianBlurImage = _libs['GraphicsMagick'].GaussianBlurImage
    GaussianBlurImage.argtypes = [POINTER(Image), c_double, c_double, POINTER(ExceptionInfo)]
    GaussianBlurImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'GaussianBlurImageChannel'):
    GaussianBlurImageChannel = _libs['GraphicsMagick'].GaussianBlurImageChannel
    GaussianBlurImageChannel.argtypes = [POINTER(Image), ChannelType, c_double, c_double, POINTER(ExceptionInfo)]
    GaussianBlurImageChannel.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'MedianFilterImage'):
    MedianFilterImage = _libs['GraphicsMagick'].MedianFilterImage
    MedianFilterImage.argtypes = [POINTER(Image), c_double, POINTER(ExceptionInfo)]
    MedianFilterImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'MotionBlurImage'):
    MotionBlurImage = _libs['GraphicsMagick'].MotionBlurImage
    MotionBlurImage.argtypes = [POINTER(Image), c_double, c_double, c_double, POINTER(ExceptionInfo)]
    MotionBlurImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'ReduceNoiseImage'):
    ReduceNoiseImage = _libs['GraphicsMagick'].ReduceNoiseImage
    ReduceNoiseImage.argtypes = [POINTER(Image), c_double, POINTER(ExceptionInfo)]
    ReduceNoiseImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'ShadeImage'):
    ShadeImage = _libs['GraphicsMagick'].ShadeImage
    ShadeImage.argtypes = [POINTER(Image), c_uint, c_double, c_double, POINTER(ExceptionInfo)]
    ShadeImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'SharpenImage'):
    SharpenImage = _libs['GraphicsMagick'].SharpenImage
    SharpenImage.argtypes = [POINTER(Image), c_double, c_double, POINTER(ExceptionInfo)]
    SharpenImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'SharpenImageChannel'):
    SharpenImageChannel = _libs['GraphicsMagick'].SharpenImageChannel
    SharpenImageChannel.argtypes = [POINTER(Image), ChannelType, c_double, c_double, POINTER(ExceptionInfo)]
    SharpenImageChannel.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'SpreadImage'):
    SpreadImage = _libs['GraphicsMagick'].SpreadImage
    SpreadImage.argtypes = [POINTER(Image), c_uint, POINTER(ExceptionInfo)]
    SpreadImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'UnsharpMaskImage'):
    UnsharpMaskImage = _libs['GraphicsMagick'].UnsharpMaskImage
    UnsharpMaskImage.argtypes = [POINTER(Image), c_double, c_double, c_double, c_double, POINTER(ExceptionInfo)]
    UnsharpMaskImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 19
if hasattr(_libs['GraphicsMagick'], 'UnsharpMaskImageChannel'):
    UnsharpMaskImageChannel = _libs['GraphicsMagick'].UnsharpMaskImageChannel
    UnsharpMaskImageChannel.argtypes = [POINTER(Image), ChannelType, c_double, c_double, c_double, c_double, POINTER(ExceptionInfo)]
    UnsharpMaskImageChannel.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 54
if hasattr(_libs['GraphicsMagick'], 'BlackThresholdImage'):
    BlackThresholdImage = _libs['GraphicsMagick'].BlackThresholdImage
    BlackThresholdImage.argtypes = [POINTER(Image), String]
    BlackThresholdImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 54
if hasattr(_libs['GraphicsMagick'], 'ChannelThresholdImage'):
    ChannelThresholdImage = _libs['GraphicsMagick'].ChannelThresholdImage
    ChannelThresholdImage.argtypes = [POINTER(Image), String]
    ChannelThresholdImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 54
if hasattr(_libs['GraphicsMagick'], 'RandomChannelThresholdImage'):
    RandomChannelThresholdImage = _libs['GraphicsMagick'].RandomChannelThresholdImage
    RandomChannelThresholdImage.argtypes = [POINTER(Image), String, String, POINTER(ExceptionInfo)]
    RandomChannelThresholdImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 54
if hasattr(_libs['GraphicsMagick'], 'ThresholdImage'):
    ThresholdImage = _libs['GraphicsMagick'].ThresholdImage
    ThresholdImage.argtypes = [POINTER(Image), c_double]
    ThresholdImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/effect.h: 54
if hasattr(_libs['GraphicsMagick'], 'WhiteThresholdImage'):
    WhiteThresholdImage = _libs['GraphicsMagick'].WhiteThresholdImage
    WhiteThresholdImage.argtypes = [POINTER(Image), String]
    WhiteThresholdImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/enhance.h: 19
if hasattr(_libs['GraphicsMagick'], 'ContrastImage'):
    ContrastImage = _libs['GraphicsMagick'].ContrastImage
    ContrastImage.argtypes = [POINTER(Image), c_uint]
    ContrastImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/enhance.h: 19
if hasattr(_libs['GraphicsMagick'], 'EqualizeImage'):
    EqualizeImage = _libs['GraphicsMagick'].EqualizeImage
    EqualizeImage.argtypes = [POINTER(Image)]
    EqualizeImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/enhance.h: 19
if hasattr(_libs['GraphicsMagick'], 'GammaImage'):
    GammaImage = _libs['GraphicsMagick'].GammaImage
    GammaImage.argtypes = [POINTER(Image), String]
    GammaImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/enhance.h: 19
if hasattr(_libs['GraphicsMagick'], 'LevelImage'):
    LevelImage = _libs['GraphicsMagick'].LevelImage
    LevelImage.argtypes = [POINTER(Image), String]
    LevelImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/enhance.h: 19
if hasattr(_libs['GraphicsMagick'], 'LevelImageChannel'):
    LevelImageChannel = _libs['GraphicsMagick'].LevelImageChannel
    LevelImageChannel.argtypes = [POINTER(Image), ChannelType, c_double, c_double, c_double]
    LevelImageChannel.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/enhance.h: 19
if hasattr(_libs['GraphicsMagick'], 'ModulateImage'):
    ModulateImage = _libs['GraphicsMagick'].ModulateImage
    ModulateImage.argtypes = [POINTER(Image), String]
    ModulateImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/enhance.h: 19
if hasattr(_libs['GraphicsMagick'], 'NegateImage'):
    NegateImage = _libs['GraphicsMagick'].NegateImage
    NegateImage.argtypes = [POINTER(Image), c_uint]
    NegateImage.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/enhance.h: 19
if hasattr(_libs['GraphicsMagick'], 'NormalizeImage'):
    NormalizeImage = _libs['GraphicsMagick'].NormalizeImage
    NormalizeImage.argtypes = [POINTER(Image)]
    NormalizeImage.restype = c_uint

magick_uint8_t = c_ubyte # gmagick_hdrs/magick/magick_types.h: 68

magick_uint16_t = c_ushort # gmagick_hdrs/magick/magick_types.h: 71

magick_uint32_t = c_uint # gmagick_hdrs/magick/magick_types.h: 75

magick_int64_t = c_long # gmagick_hdrs/magick/magick_types.h: 78

magick_off_t = magick_int64_t # gmagick_hdrs/magick/magick_types.h: 92

enum_anon_34 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 34

UndefinedVirtualPixelMethod = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 34

ConstantVirtualPixelMethod = (UndefinedVirtualPixelMethod + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 34

EdgeVirtualPixelMethod = (ConstantVirtualPixelMethod + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 34

MirrorVirtualPixelMethod = (EdgeVirtualPixelMethod + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 34

TileVirtualPixelMethod = (MirrorVirtualPixelMethod + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 34

VirtualPixelMethod = enum_anon_34 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 34

Cache = _CacheInfoPtr_ # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 39

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 51
if hasattr(_libs['GraphicsMagick'], 'AcquireImagePixels'):
    AcquireImagePixels = _libs['GraphicsMagick'].AcquireImagePixels
    AcquireImagePixels.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    AcquireImagePixels.restype = POINTER(PixelPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 61
if hasattr(_libs['GraphicsMagick'], 'AccessImmutableIndexes'):
    AccessImmutableIndexes = _libs['GraphicsMagick'].AccessImmutableIndexes
    AccessImmutableIndexes.argtypes = [POINTER(Image)]
    AccessImmutableIndexes.restype = POINTER(IndexPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 69
if hasattr(_libs['GraphicsMagick'], 'AcquireOnePixel'):
    AcquireOnePixel = _libs['GraphicsMagick'].AcquireOnePixel
    AcquireOnePixel.argtypes = [POINTER(Image), c_long, c_long, POINTER(ExceptionInfo)]
    AcquireOnePixel.restype = PixelPacket

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 78
if hasattr(_libs['GraphicsMagick'], 'GetImagePixels'):
    GetImagePixels = _libs['GraphicsMagick'].GetImagePixels
    GetImagePixels.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong]
    GetImagePixels.restype = POINTER(PixelPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 81
if hasattr(_libs['GraphicsMagick'], 'GetImagePixelsEx'):
    GetImagePixelsEx = _libs['GraphicsMagick'].GetImagePixelsEx
    GetImagePixelsEx.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    GetImagePixelsEx.restype = POINTER(PixelPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 90
if hasattr(_libs['GraphicsMagick'], 'GetImageVirtualPixelMethod'):
    GetImageVirtualPixelMethod = _libs['GraphicsMagick'].GetImageVirtualPixelMethod
    GetImageVirtualPixelMethod.argtypes = [POINTER(Image)]
    GetImageVirtualPixelMethod.restype = VirtualPixelMethod

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 97
if hasattr(_libs['GraphicsMagick'], 'GetPixels'):
    GetPixels = _libs['GraphicsMagick'].GetPixels
    GetPixels.argtypes = [POINTER(Image)]
    GetPixels.restype = POINTER(PixelPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 99
if hasattr(_libs['GraphicsMagick'], 'AccessMutablePixels'):
    AccessMutablePixels = _libs['GraphicsMagick'].AccessMutablePixels
    AccessMutablePixels.argtypes = [POINTER(Image)]
    AccessMutablePixels.restype = POINTER(PixelPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 107
if hasattr(_libs['GraphicsMagick'], 'GetIndexes'):
    GetIndexes = _libs['GraphicsMagick'].GetIndexes
    GetIndexes.argtypes = [POINTER(Image)]
    GetIndexes.restype = POINTER(IndexPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 109
if hasattr(_libs['GraphicsMagick'], 'AccessMutableIndexes'):
    AccessMutableIndexes = _libs['GraphicsMagick'].AccessMutableIndexes
    AccessMutableIndexes.argtypes = [POINTER(Image)]
    AccessMutableIndexes.restype = POINTER(IndexPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 119
if hasattr(_libs['GraphicsMagick'], 'GetOnePixel'):
    GetOnePixel = _libs['GraphicsMagick'].GetOnePixel
    GetOnePixel.argtypes = [POINTER(Image), c_long, c_long]
    GetOnePixel.restype = PixelPacket

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 126
if hasattr(_libs['GraphicsMagick'], 'GetPixelCacheArea'):
    GetPixelCacheArea = _libs['GraphicsMagick'].GetPixelCacheArea
    GetPixelCacheArea.argtypes = [POINTER(Image)]
    GetPixelCacheArea.restype = magick_off_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 133
if hasattr(_libs['GraphicsMagick'], 'SetImagePixels'):
    SetImagePixels = _libs['GraphicsMagick'].SetImagePixels
    SetImagePixels.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong]
    SetImagePixels.restype = POINTER(PixelPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 136
if hasattr(_libs['GraphicsMagick'], 'SetImagePixelsEx'):
    SetImagePixelsEx = _libs['GraphicsMagick'].SetImagePixelsEx
    SetImagePixelsEx.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    SetImagePixelsEx.restype = POINTER(PixelPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 145
if hasattr(_libs['GraphicsMagick'], 'SetImageVirtualPixelMethod'):
    SetImageVirtualPixelMethod = _libs['GraphicsMagick'].SetImageVirtualPixelMethod
    SetImageVirtualPixelMethod.argtypes = [POINTER(Image), VirtualPixelMethod]
    SetImageVirtualPixelMethod.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 153
if hasattr(_libs['GraphicsMagick'], 'SyncImagePixels'):
    SyncImagePixels = _libs['GraphicsMagick'].SyncImagePixels
    SyncImagePixels.argtypes = [POINTER(Image)]
    SyncImagePixels.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 155
if hasattr(_libs['GraphicsMagick'], 'SyncImagePixelsEx'):
    SyncImagePixelsEx = _libs['GraphicsMagick'].SyncImagePixelsEx
    SyncImagePixelsEx.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    SyncImagePixelsEx.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 167
if hasattr(_libs['GraphicsMagick'], 'OpenCacheView'):
    OpenCacheView = _libs['GraphicsMagick'].OpenCacheView
    OpenCacheView.argtypes = [POINTER(Image)]
    OpenCacheView.restype = POINTER(ViewInfo)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 173
if hasattr(_libs['GraphicsMagick'], 'CloseCacheView'):
    CloseCacheView = _libs['GraphicsMagick'].CloseCacheView
    CloseCacheView.argtypes = [POINTER(ViewInfo)]
    CloseCacheView.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 182
if hasattr(_libs['GraphicsMagick'], 'AccessCacheViewPixels'):
    AccessCacheViewPixels = _libs['GraphicsMagick'].AccessCacheViewPixels
    AccessCacheViewPixels.argtypes = [POINTER(ViewInfo)]
    AccessCacheViewPixels.restype = POINTER(PixelPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 189
if hasattr(_libs['GraphicsMagick'], 'AcquireCacheViewIndexes'):
    AcquireCacheViewIndexes = _libs['GraphicsMagick'].AcquireCacheViewIndexes
    AcquireCacheViewIndexes.argtypes = [POINTER(ViewInfo)]
    AcquireCacheViewIndexes.restype = POINTER(IndexPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 196
if hasattr(_libs['GraphicsMagick'], 'AcquireCacheViewPixels'):
    AcquireCacheViewPixels = _libs['GraphicsMagick'].AcquireCacheViewPixels
    AcquireCacheViewPixels.argtypes = [POINTER(ViewInfo), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    AcquireCacheViewPixels.restype = POINTER(PixelPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 208
if hasattr(_libs['GraphicsMagick'], 'AcquireOneCacheViewPixel'):
    AcquireOneCacheViewPixel = _libs['GraphicsMagick'].AcquireOneCacheViewPixel
    AcquireOneCacheViewPixel.argtypes = [POINTER(ViewInfo), POINTER(PixelPacket), c_long, c_long, POINTER(ExceptionInfo)]
    AcquireOneCacheViewPixel.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 216
if hasattr(_libs['GraphicsMagick'], 'GetCacheViewArea'):
    GetCacheViewArea = _libs['GraphicsMagick'].GetCacheViewArea
    GetCacheViewArea.argtypes = [POINTER(ViewInfo)]
    GetCacheViewArea.restype = magick_off_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 221
if hasattr(_libs['GraphicsMagick'], 'GetCacheViewImage'):
    GetCacheViewImage = _libs['GraphicsMagick'].GetCacheViewImage
    GetCacheViewImage.argtypes = [POINTER(ViewInfo)]
    GetCacheViewImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 228
if hasattr(_libs['GraphicsMagick'], 'GetCacheViewIndexes'):
    GetCacheViewIndexes = _libs['GraphicsMagick'].GetCacheViewIndexes
    GetCacheViewIndexes.argtypes = [POINTER(ViewInfo)]
    GetCacheViewIndexes.restype = POINTER(IndexPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 235
if hasattr(_libs['GraphicsMagick'], 'GetCacheViewPixels'):
    GetCacheViewPixels = _libs['GraphicsMagick'].GetCacheViewPixels
    GetCacheViewPixels.argtypes = [POINTER(ViewInfo), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    GetCacheViewPixels.restype = POINTER(PixelPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 243
if hasattr(_libs['GraphicsMagick'], 'GetCacheViewRegion'):
    GetCacheViewRegion = _libs['GraphicsMagick'].GetCacheViewRegion
    GetCacheViewRegion.argtypes = [POINTER(ViewInfo)]
    GetCacheViewRegion.restype = RectangleInfo

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 251
if hasattr(_libs['GraphicsMagick'], 'SetCacheViewPixels'):
    SetCacheViewPixels = _libs['GraphicsMagick'].SetCacheViewPixels
    SetCacheViewPixels.argtypes = [POINTER(ViewInfo), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    SetCacheViewPixels.restype = POINTER(PixelPacket)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/pixel_cache.h: 259
if hasattr(_libs['GraphicsMagick'], 'SyncCacheViewPixels'):
    SyncCacheViewPixels = _libs['GraphicsMagick'].SyncCacheViewPixels
    SyncCacheViewPixels.argtypes = [POINTER(ViewInfo), POINTER(ExceptionInfo)]
    SyncCacheViewPixels.restype = c_uint

BlobInfo = struct__BlobInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 29

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 41
if hasattr(_libs['GraphicsMagick'], 'CloneBlobInfo'):
    CloneBlobInfo = _libs['GraphicsMagick'].CloneBlobInfo
    CloneBlobInfo.argtypes = [POINTER(BlobInfo)]
    CloneBlobInfo.restype = POINTER(BlobInfo)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 47
if hasattr(_libs['GraphicsMagick'], 'ReferenceBlob'):
    ReferenceBlob = _libs['GraphicsMagick'].ReferenceBlob
    ReferenceBlob.argtypes = [POINTER(BlobInfo)]
    ReferenceBlob.restype = POINTER(BlobInfo)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 52
if hasattr(_libs['GraphicsMagick'], 'DestroyBlobInfo'):
    DestroyBlobInfo = _libs['GraphicsMagick'].DestroyBlobInfo
    DestroyBlobInfo.argtypes = [POINTER(BlobInfo)]
    DestroyBlobInfo.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 58
if hasattr(_libs['GraphicsMagick'], 'DetachBlob'):
    DetachBlob = _libs['GraphicsMagick'].DetachBlob
    DetachBlob.argtypes = [POINTER(BlobInfo)]
    DetachBlob.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 63
if hasattr(_libs['GraphicsMagick'], 'GetBlobInfo'):
    GetBlobInfo = _libs['GraphicsMagick'].GetBlobInfo
    GetBlobInfo.argtypes = [POINTER(BlobInfo)]
    GetBlobInfo.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 68
if hasattr(_libs['GraphicsMagick'], 'AttachBlob'):
    AttachBlob = _libs['GraphicsMagick'].AttachBlob
    AttachBlob.argtypes = [POINTER(BlobInfo), POINTER(None), c_size_t]
    AttachBlob.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 81
if hasattr(_libs['GraphicsMagick'], 'DestroyBlob'):
    DestroyBlob = _libs['GraphicsMagick'].DestroyBlob
    DestroyBlob.argtypes = [POINTER(Image)]
    DestroyBlob.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 93
if hasattr(_libs['GraphicsMagick'], 'BlobToImage'):
    BlobToImage = _libs['GraphicsMagick'].BlobToImage
    BlobToImage.argtypes = [POINTER(ImageInfo), POINTER(None), c_size_t, POINTER(ExceptionInfo)]
    BlobToImage.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 103
if hasattr(_libs['GraphicsMagick'], 'PingBlob'):
    PingBlob = _libs['GraphicsMagick'].PingBlob
    PingBlob.argtypes = [POINTER(ImageInfo), POINTER(None), c_size_t, POINTER(ExceptionInfo)]
    PingBlob.restype = POINTER(Image)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 112
if hasattr(_libs['GraphicsMagick'], 'ImageToBlob'):
    ImageToBlob = _libs['GraphicsMagick'].ImageToBlob
    ImageToBlob.argtypes = [POINTER(ImageInfo), POINTER(Image), POINTER(c_size_t), POINTER(ExceptionInfo)]
    ImageToBlob.restype = POINTER(None)

enum_anon_35 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 133

UndefinedBlobMode = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 133

ReadBlobMode = (UndefinedBlobMode + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 133

ReadBinaryBlobMode = (ReadBlobMode + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 133

WriteBlobMode = (ReadBinaryBlobMode + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 133

WriteBinaryBlobMode = (WriteBlobMode + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 133

BlobMode = enum_anon_35 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 133

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 139
if hasattr(_libs['GraphicsMagick'], 'OpenBlob'):
    OpenBlob = _libs['GraphicsMagick'].OpenBlob
    OpenBlob.argtypes = [POINTER(ImageInfo), POINTER(Image), BlobMode, POINTER(ExceptionInfo)]
    OpenBlob.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 147
if hasattr(_libs['GraphicsMagick'], 'CloseBlob'):
    CloseBlob = _libs['GraphicsMagick'].CloseBlob
    CloseBlob.argtypes = [POINTER(Image)]
    CloseBlob.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 153
if hasattr(_libs['GraphicsMagick'], 'ReadBlob'):
    ReadBlob = _libs['GraphicsMagick'].ReadBlob
    ReadBlob.argtypes = [POINTER(Image), c_size_t, POINTER(None)]
    ReadBlob.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 161
if hasattr(_libs['GraphicsMagick'], 'ReadBlobZC'):
    ReadBlobZC = _libs['GraphicsMagick'].ReadBlobZC
    ReadBlobZC.argtypes = [POINTER(Image), c_size_t, POINTER(POINTER(None))]
    ReadBlobZC.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 168
if hasattr(_libs['GraphicsMagick'], 'WriteBlob'):
    WriteBlob = _libs['GraphicsMagick'].WriteBlob
    WriteBlob.argtypes = [POINTER(Image), c_size_t, POINTER(None)]
    WriteBlob.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 175
if hasattr(_libs['GraphicsMagick'], 'SeekBlob'):
    SeekBlob = _libs['GraphicsMagick'].SeekBlob
    SeekBlob.argtypes = [POINTER(Image), magick_off_t, c_int]
    SeekBlob.restype = magick_off_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 183
if hasattr(_libs['GraphicsMagick'], 'TellBlob'):
    TellBlob = _libs['GraphicsMagick'].TellBlob
    TellBlob.argtypes = [POINTER(Image)]
    TellBlob.restype = magick_off_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 188
if hasattr(_libs['GraphicsMagick'], 'EOFBlob'):
    EOFBlob = _libs['GraphicsMagick'].EOFBlob
    EOFBlob.argtypes = [POINTER(Image)]
    EOFBlob.restype = c_int

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 194
if hasattr(_libs['GraphicsMagick'], 'GetBlobStatus'):
    GetBlobStatus = _libs['GraphicsMagick'].GetBlobStatus
    GetBlobStatus.argtypes = [POINTER(Image)]
    GetBlobStatus.restype = c_int

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 200
if hasattr(_libs['GraphicsMagick'], 'GetBlobSize'):
    GetBlobSize = _libs['GraphicsMagick'].GetBlobSize
    GetBlobSize.argtypes = [POINTER(Image)]
    GetBlobSize.restype = magick_off_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 206
if hasattr(_libs['GraphicsMagick'], 'GetBlobFileHandle'):
    GetBlobFileHandle = _libs['GraphicsMagick'].GetBlobFileHandle
    GetBlobFileHandle.argtypes = [POINTER(Image)]
    GetBlobFileHandle.restype = POINTER(FILE)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 213
if hasattr(_libs['GraphicsMagick'], 'GetBlobStreamData'):
    GetBlobStreamData = _libs['GraphicsMagick'].GetBlobStreamData
    GetBlobStreamData.argtypes = [POINTER(Image)]
    GetBlobStreamData.restype = POINTER(c_ubyte)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 226
if hasattr(_libs['GraphicsMagick'], 'ReadBlobByte'):
    ReadBlobByte = _libs['GraphicsMagick'].ReadBlobByte
    ReadBlobByte.argtypes = [POINTER(Image)]
    ReadBlobByte.restype = c_int

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 232
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBShort'):
    ReadBlobLSBShort = _libs['GraphicsMagick'].ReadBlobLSBShort
    ReadBlobLSBShort.argtypes = [POINTER(Image)]
    ReadBlobLSBShort.restype = magick_uint16_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 238
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBShorts'):
    ReadBlobLSBShorts = _libs['GraphicsMagick'].ReadBlobLSBShorts
    ReadBlobLSBShorts.argtypes = [POINTER(Image), c_size_t, POINTER(magick_uint16_t)]
    ReadBlobLSBShorts.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 245
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBShort'):
    ReadBlobMSBShort = _libs['GraphicsMagick'].ReadBlobMSBShort
    ReadBlobMSBShort.argtypes = [POINTER(Image)]
    ReadBlobMSBShort.restype = magick_uint16_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 251
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBShorts'):
    ReadBlobMSBShorts = _libs['GraphicsMagick'].ReadBlobMSBShorts
    ReadBlobMSBShorts.argtypes = [POINTER(Image), c_size_t, POINTER(magick_uint16_t)]
    ReadBlobMSBShorts.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 257
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBLong'):
    ReadBlobLSBLong = _libs['GraphicsMagick'].ReadBlobLSBLong
    ReadBlobLSBLong.argtypes = [POINTER(Image)]
    ReadBlobLSBLong.restype = magick_uint32_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 263
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBLongs'):
    ReadBlobLSBLongs = _libs['GraphicsMagick'].ReadBlobLSBLongs
    ReadBlobLSBLongs.argtypes = [POINTER(Image), c_size_t, POINTER(magick_uint32_t)]
    ReadBlobLSBLongs.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 269
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBLong'):
    ReadBlobMSBLong = _libs['GraphicsMagick'].ReadBlobMSBLong
    ReadBlobMSBLong.argtypes = [POINTER(Image)]
    ReadBlobMSBLong.restype = magick_uint32_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 274
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBLongs'):
    ReadBlobMSBLongs = _libs['GraphicsMagick'].ReadBlobMSBLongs
    ReadBlobMSBLongs.argtypes = [POINTER(Image), c_size_t, POINTER(magick_uint32_t)]
    ReadBlobMSBLongs.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 280
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBFloat'):
    ReadBlobLSBFloat = _libs['GraphicsMagick'].ReadBlobLSBFloat
    ReadBlobLSBFloat.argtypes = [POINTER(Image)]
    ReadBlobLSBFloat.restype = c_float

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 286
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBFloats'):
    ReadBlobLSBFloats = _libs['GraphicsMagick'].ReadBlobLSBFloats
    ReadBlobLSBFloats.argtypes = [POINTER(Image), c_size_t, POINTER(c_float)]
    ReadBlobLSBFloats.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 292
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBFloat'):
    ReadBlobMSBFloat = _libs['GraphicsMagick'].ReadBlobMSBFloat
    ReadBlobMSBFloat.argtypes = [POINTER(Image)]
    ReadBlobMSBFloat.restype = c_float

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 298
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBFloats'):
    ReadBlobMSBFloats = _libs['GraphicsMagick'].ReadBlobMSBFloats
    ReadBlobMSBFloats.argtypes = [POINTER(Image), c_size_t, POINTER(c_float)]
    ReadBlobMSBFloats.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 304
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBDouble'):
    ReadBlobLSBDouble = _libs['GraphicsMagick'].ReadBlobLSBDouble
    ReadBlobLSBDouble.argtypes = [POINTER(Image)]
    ReadBlobLSBDouble.restype = c_double

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 310
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBDoubles'):
    ReadBlobLSBDoubles = _libs['GraphicsMagick'].ReadBlobLSBDoubles
    ReadBlobLSBDoubles.argtypes = [POINTER(Image), c_size_t, POINTER(c_double)]
    ReadBlobLSBDoubles.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 316
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBDouble'):
    ReadBlobMSBDouble = _libs['GraphicsMagick'].ReadBlobMSBDouble
    ReadBlobMSBDouble.argtypes = [POINTER(Image)]
    ReadBlobMSBDouble.restype = c_double

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 321
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBDoubles'):
    ReadBlobMSBDoubles = _libs['GraphicsMagick'].ReadBlobMSBDoubles
    ReadBlobMSBDoubles.argtypes = [POINTER(Image), c_size_t, POINTER(c_double)]
    ReadBlobMSBDoubles.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 328
if hasattr(_libs['GraphicsMagick'], 'ReadBlobString'):
    ReadBlobString = _libs['GraphicsMagick'].ReadBlobString
    ReadBlobString.argtypes = [POINTER(Image), String]
    if sizeof(c_int) == sizeof(c_void_p):
        ReadBlobString.restype = ReturnString
    else:
        ReadBlobString.restype = String
        ReadBlobString.errcheck = ReturnString

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 334
if hasattr(_libs['GraphicsMagick'], 'WriteBlobByte'):
    WriteBlobByte = _libs['GraphicsMagick'].WriteBlobByte
    WriteBlobByte.argtypes = [POINTER(Image), magick_uint8_t]
    WriteBlobByte.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 340
if hasattr(_libs['GraphicsMagick'], 'WriteBlobFile'):
    WriteBlobFile = _libs['GraphicsMagick'].WriteBlobFile
    WriteBlobFile.argtypes = [POINTER(Image), String]
    WriteBlobFile.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 346
if hasattr(_libs['GraphicsMagick'], 'WriteBlobLSBShort'):
    WriteBlobLSBShort = _libs['GraphicsMagick'].WriteBlobLSBShort
    WriteBlobLSBShort.argtypes = [POINTER(Image), magick_uint16_t]
    WriteBlobLSBShort.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 352
if hasattr(_libs['GraphicsMagick'], 'WriteBlobLSBLong'):
    WriteBlobLSBLong = _libs['GraphicsMagick'].WriteBlobLSBLong
    WriteBlobLSBLong.argtypes = [POINTER(Image), magick_uint32_t]
    WriteBlobLSBLong.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 360
if hasattr(_libs['GraphicsMagick'], 'WriteBlobMSBLong'):
    WriteBlobMSBLong = _libs['GraphicsMagick'].WriteBlobMSBLong
    WriteBlobMSBLong.argtypes = [POINTER(Image), magick_uint32_t]
    WriteBlobMSBLong.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 366
if hasattr(_libs['GraphicsMagick'], 'WriteBlobMSBShort'):
    WriteBlobMSBShort = _libs['GraphicsMagick'].WriteBlobMSBShort
    WriteBlobMSBShort.argtypes = [POINTER(Image), magick_uint16_t]
    WriteBlobMSBShort.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 373
if hasattr(_libs['GraphicsMagick'], 'WriteBlobString'):
    WriteBlobString = _libs['GraphicsMagick'].WriteBlobString
    WriteBlobString.argtypes = [POINTER(Image), String]
    WriteBlobString.restype = c_size_t

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 386
if hasattr(_libs['GraphicsMagick'], 'BlobIsSeekable'):
    BlobIsSeekable = _libs['GraphicsMagick'].BlobIsSeekable
    BlobIsSeekable.argtypes = [POINTER(Image)]
    BlobIsSeekable.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 391
if hasattr(_libs['GraphicsMagick'], 'SetBlobClosable'):
    SetBlobClosable = _libs['GraphicsMagick'].SetBlobClosable
    SetBlobClosable.argtypes = [POINTER(Image), c_uint]
    SetBlobClosable.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 397
if hasattr(_libs['GraphicsMagick'], 'SetBlobTemporary'):
    SetBlobTemporary = _libs['GraphicsMagick'].SetBlobTemporary
    SetBlobTemporary.argtypes = [POINTER(Image), c_uint]
    SetBlobTemporary.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 404
if hasattr(_libs['GraphicsMagick'], 'GetBlobTemporary'):
    GetBlobTemporary = _libs['GraphicsMagick'].GetBlobTemporary
    GetBlobTemporary.argtypes = [POINTER(Image)]
    GetBlobTemporary.restype = c_uint

enum_anon_36 = c_int # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 420

ReadMode = 0 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 420

WriteMode = (ReadMode + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 420

IOMode = (WriteMode + 1) # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 420

MapMode = enum_anon_36 # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 420

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 425
if hasattr(_libs['GraphicsMagick'], 'UnmapBlob'):
    UnmapBlob = _libs['GraphicsMagick'].UnmapBlob
    UnmapBlob.argtypes = [POINTER(None), c_size_t]
    UnmapBlob.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 431
if hasattr(_libs['GraphicsMagick'], 'MapBlob'):
    MapBlob = _libs['GraphicsMagick'].MapBlob
    MapBlob.argtypes = [c_int, MapMode, magick_off_t, c_size_t]
    MapBlob.restype = POINTER(None)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 445
if hasattr(_libs['GraphicsMagick'], 'BlobToFile'):
    BlobToFile = _libs['GraphicsMagick'].BlobToFile
    BlobToFile.argtypes = [String, POINTER(None), c_size_t, POINTER(ExceptionInfo)]
    BlobToFile.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 453
if hasattr(_libs['GraphicsMagick'], 'FileToBlob'):
    FileToBlob = _libs['GraphicsMagick'].FileToBlob
    FileToBlob.argtypes = [String, POINTER(c_size_t), POINTER(ExceptionInfo)]
    FileToBlob.restype = POINTER(None)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 466
if hasattr(_libs['GraphicsMagick'], 'BlobReserveSize'):
    BlobReserveSize = _libs['GraphicsMagick'].BlobReserveSize
    BlobReserveSize.argtypes = [POINTER(Image), magick_off_t]
    BlobReserveSize.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 472
if hasattr(_libs['GraphicsMagick'], 'ImageToFile'):
    ImageToFile = _libs['GraphicsMagick'].ImageToFile
    ImageToFile.argtypes = [POINTER(Image), String, POINTER(ExceptionInfo)]
    ImageToFile.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 480
if hasattr(_libs['GraphicsMagick'], 'GetConfigureBlob'):
    GetConfigureBlob = _libs['GraphicsMagick'].GetConfigureBlob
    GetConfigureBlob.argtypes = [String, String, POINTER(c_size_t), POINTER(ExceptionInfo)]
    GetConfigureBlob.restype = POINTER(None)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 489
if hasattr(_libs['GraphicsMagick'], 'MSBOrderLong'):
    MSBOrderLong = _libs['GraphicsMagick'].MSBOrderLong
    MSBOrderLong.argtypes = [POINTER(c_ubyte), c_size_t]
    MSBOrderLong.restype = None

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 496
if hasattr(_libs['GraphicsMagick'], 'MSBOrderShort'):
    MSBOrderShort = _libs['GraphicsMagick'].MSBOrderShort
    MSBOrderShort.argtypes = [POINTER(c_ubyte), c_size_t]
    MSBOrderShort.restype = None

struct__ImageAttribute.__slots__ = [
    'key',
    'value',
    'length',
    'previous',
    'next',
]
struct__ImageAttribute._fields_ = [
    ('key', String),
    ('value', String),
    ('length', c_size_t),
    ('previous', POINTER(struct__ImageAttribute)),
    ('next', POINTER(struct__ImageAttribute)),
]

ImageAttribute = struct__ImageAttribute # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/attribute.h: 32

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/attribute.h: 38
if hasattr(_libs['GraphicsMagick'], 'GetImageAttribute'):
    GetImageAttribute = _libs['GraphicsMagick'].GetImageAttribute
    GetImageAttribute.argtypes = [POINTER(Image), String]
    GetImageAttribute.restype = POINTER(ImageAttribute)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/attribute.h: 38
if hasattr(_libs['GraphicsMagick'], 'GetImageClippingPathAttribute'):
    GetImageClippingPathAttribute = _libs['GraphicsMagick'].GetImageClippingPathAttribute
    GetImageClippingPathAttribute.argtypes = [POINTER(Image)]
    GetImageClippingPathAttribute.restype = POINTER(ImageAttribute)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/attribute.h: 38
if hasattr(_libs['GraphicsMagick'], 'GetImageInfoAttribute'):
    GetImageInfoAttribute = _libs['GraphicsMagick'].GetImageInfoAttribute
    GetImageInfoAttribute.argtypes = [POINTER(ImageInfo), POINTER(Image), String]
    GetImageInfoAttribute.restype = POINTER(ImageAttribute)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/attribute.h: 43
if hasattr(_libs['GraphicsMagick'], 'CloneImageAttributes'):
    CloneImageAttributes = _libs['GraphicsMagick'].CloneImageAttributes
    CloneImageAttributes.argtypes = [POINTER(Image), POINTER(Image)]
    CloneImageAttributes.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/attribute.h: 43
if hasattr(_libs['GraphicsMagick'], 'SetImageAttribute'):
    SetImageAttribute = _libs['GraphicsMagick'].SetImageAttribute
    SetImageAttribute.argtypes = [POINTER(Image), String, String]
    SetImageAttribute.restype = c_uint

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/attribute.h: 47
if hasattr(_libs['GraphicsMagick'], 'DestroyImageAttributes'):
    DestroyImageAttributes = _libs['GraphicsMagick'].DestroyImageAttributes
    DestroyImageAttributes.argtypes = [POINTER(Image)]
    DestroyImageAttributes.restype = None

# gmagick_hdrs/magick/magick_config.h: 22
try:
    MaxRGB = 255
except:
    pass

# gmagick_hdrs/magick/magick_config.h: 23
try:
    MaxRGBFloat = 255.0
except:
    pass

# gmagick_hdrs/magick/magick_config.h: 24
try:
    MaxRGBDouble = 255.0
except:
    pass

# gmagick_hdrs/magick/common.h: 101
try:
    MagickFalse = 0
except:
    pass

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 38
def MaxValueGivenBits(bits):
    return ((1L << (bits - 1)) + ((1L << (bits - 1)) - 1))

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 41
try:
    OpaqueOpacity = 0L
except:
    pass

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 42
try:
    TransparentOpacity = MaxRGB
except:
    pass

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 43
def RoundDoubleToQuantum(value):
    return (value < 0.0) and 0 or (value > MaxRGBDouble) and MaxRGB or (value + 0.5)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 45
def RoundFloatToQuantum(value):
    return (value < 0.0) and 0 or (value > MaxRGBFloat) and MaxRGB or (value + 0.5)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 47
def ConstrainToRange(min, max, value):
    return (value < min) and min or (value > max) and max or value

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 49
def ConstrainToQuantum(value):
    return (ConstrainToRange (0, MaxRGB, value))

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 50
def ScaleAnyToQuantum(x, max_value):
    return (((MaxRGBDouble * x) / max_value) + 0.5)

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 52
def MagickBoolToString(value):
    return (value != MagickFalse) and 'True' or 'False'

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 58
def MagickChannelEnabled(channels, channel):
    return ((channels == AllChannels) or (channels == channel))

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 63
try:
    RunlengthEncodedCompression = RLECompression
except:
    pass

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 64
def RoundSignedToQuantum(value):
    return (RoundDoubleToQuantum (value))

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 65
def RoundToQuantum(value):
    return (RoundDoubleToQuantum (value))

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 431
try:
    MAGICK_PIXELS_BGRA = 1
except:
    pass

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/resize.h: 18
try:
    DefaultResizeFilter = LanczosFilter
except:
    pass

# /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/blob.h: 24
try:
    MinBlobExtent = 32768L
except:
    pass

_Image = struct__Image # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 553

_ImageAttribute = struct__ImageAttribute # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/attribute.h: 20

_ExceptionInfo = struct__ExceptionInfo # gmagick_hdrs/magick/error.h: 230

_AffineMatrix = struct__AffineMatrix # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 363

_PrimaryInfo = struct__PrimaryInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 371

_ChromaticityInfo = struct__ChromaticityInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 380

_PixelPacket = struct__PixelPacket # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 438

_DoublePixelPacket = struct__DoublePixelPacket # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 447

_ErrorInfo = struct__ErrorInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 459

_FrameInfo = struct__FrameInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 472

_LongPixelPacket = struct__LongPixelPacket # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 483

_MontageInfo = struct__MontageInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 519

_ProfileInfo = struct__ProfileInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 531

_RectangleInfo = struct__RectangleInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 542

_SegmentInfo = struct__SegmentInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 551

_ImageInfo = struct__ImageInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/image.h: 880

_MagickInfo = struct__MagickInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/magick.h: 46

_ExportPixelAreaOptions = struct__ExportPixelAreaOptions # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 97

_ExportPixelAreaInfo = struct__ExportPixelAreaInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 107

_ImportPixelAreaOptions = struct__ImportPixelAreaOptions # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 129

_ImportPixelAreaInfo = struct__ImportPixelAreaInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/constitute.h: 139

_DelegateInfo = struct__DelegateInfo # /home/rainman/Dropbox/pygm-light/gmagick_hdrs/magick/delegate.h: 21

# No inserted files

