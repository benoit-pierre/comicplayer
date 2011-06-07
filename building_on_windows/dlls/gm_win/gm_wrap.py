'''Wrapper for image.h

Generated with:
generate_wrapper.py

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

_libs["GraphicsMagick"] = load_library("CORE_RL_magick_")

# 1 libraries
# End libraries

# No modules

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

Quantum = c_ubyte # gm_headers/magick/magick_config.h: 38

# /tmp/tmpu80Elu/image.h: 649
class struct__Image(Structure):
    pass

# gm_headers/magick/forward.h: 20
class struct__Ascii85Info(Structure):
    pass

_Ascii85InfoPtr_ = POINTER(struct__Ascii85Info) # gm_headers/magick/forward.h: 20

# gm_headers/magick/forward.h: 22
class struct__BlobInfo(Structure):
    pass

_BlobInfoPtr_ = POINTER(struct__BlobInfo) # gm_headers/magick/forward.h: 22

# gm_headers/magick/forward.h: 24
class struct__CacheInfo(Structure):
    pass

_CacheInfoPtr_ = POINTER(struct__CacheInfo) # gm_headers/magick/forward.h: 24

# /tmp/tmpu80Elu/attribute.h: 28
class struct__ImageAttribute(Structure):
    pass

_ImageAttributePtr_ = POINTER(struct__ImageAttribute) # gm_headers/magick/forward.h: 26

# gm_headers/magick/forward.h: 28
class struct__SemaphoreInfo(Structure):
    pass

_SemaphoreInfoPtr_ = POINTER(struct__SemaphoreInfo) # gm_headers/magick/forward.h: 28

# gm_headers/magick/forward.h: 30
class struct__ThreadViewSet(Structure):
    pass

_ThreadViewSetPtr_ = POINTER(struct__ThreadViewSet) # gm_headers/magick/forward.h: 30

ViewInfo = POINTER(None) # gm_headers/magick/forward.h: 32

magick_uint8_t = c_ubyte # gm_headers/magick/magick_types.h: 68

magick_uint16_t = c_ushort # gm_headers/magick/magick_types.h: 71

magick_uint32_t = c_uint # gm_headers/magick/magick_types.h: 75

magick_int64_t = c_longlong # gm_headers/magick/magick_types.h: 78

magick_off_t = magick_int64_t # gm_headers/magick/magick_types.h: 92

enum_anon_6 = c_int # gm_headers/magick/error.h: 54

UndefinedExceptionBase = 0 # gm_headers/magick/error.h: 54

ExceptionBase = 1 # gm_headers/magick/error.h: 54

ResourceBase = 2 # gm_headers/magick/error.h: 54

ResourceLimitBase = 2 # gm_headers/magick/error.h: 54

TypeBase = 5 # gm_headers/magick/error.h: 54

AnnotateBase = 5 # gm_headers/magick/error.h: 54

OptionBase = 10 # gm_headers/magick/error.h: 54

DelegateBase = 15 # gm_headers/magick/error.h: 54

MissingDelegateBase = 20 # gm_headers/magick/error.h: 54

CorruptImageBase = 25 # gm_headers/magick/error.h: 54

FileOpenBase = 30 # gm_headers/magick/error.h: 54

BlobBase = 35 # gm_headers/magick/error.h: 54

StreamBase = 40 # gm_headers/magick/error.h: 54

CacheBase = 45 # gm_headers/magick/error.h: 54

CoderBase = 50 # gm_headers/magick/error.h: 54

ModuleBase = 55 # gm_headers/magick/error.h: 54

DrawBase = 60 # gm_headers/magick/error.h: 54

RenderBase = 60 # gm_headers/magick/error.h: 54

ImageBase = 65 # gm_headers/magick/error.h: 54

WandBase = 67 # gm_headers/magick/error.h: 54

TemporaryFileBase = 70 # gm_headers/magick/error.h: 54

TransformBase = 75 # gm_headers/magick/error.h: 54

XServerBase = 80 # gm_headers/magick/error.h: 54

X11Base = 81 # gm_headers/magick/error.h: 54

UserBase = 82 # gm_headers/magick/error.h: 54

MonitorBase = 85 # gm_headers/magick/error.h: 54

LocaleBase = 86 # gm_headers/magick/error.h: 54

DeprecateBase = 87 # gm_headers/magick/error.h: 54

RegistryBase = 90 # gm_headers/magick/error.h: 54

ConfigureBase = 95 # gm_headers/magick/error.h: 54

ExceptionBaseType = enum_anon_6 # gm_headers/magick/error.h: 54

enum_anon_7 = c_int # gm_headers/magick/error.h: 182

UndefinedException = 0 # gm_headers/magick/error.h: 182

EventException = 100 # gm_headers/magick/error.h: 182

ExceptionEvent = (EventException + ExceptionBase) # gm_headers/magick/error.h: 182

ResourceEvent = (EventException + ResourceBase) # gm_headers/magick/error.h: 182

ResourceLimitEvent = (EventException + ResourceLimitBase) # gm_headers/magick/error.h: 182

TypeEvent = (EventException + TypeBase) # gm_headers/magick/error.h: 182

AnnotateEvent = (EventException + AnnotateBase) # gm_headers/magick/error.h: 182

OptionEvent = (EventException + OptionBase) # gm_headers/magick/error.h: 182

DelegateEvent = (EventException + DelegateBase) # gm_headers/magick/error.h: 182

MissingDelegateEvent = (EventException + MissingDelegateBase) # gm_headers/magick/error.h: 182

CorruptImageEvent = (EventException + CorruptImageBase) # gm_headers/magick/error.h: 182

FileOpenEvent = (EventException + FileOpenBase) # gm_headers/magick/error.h: 182

BlobEvent = (EventException + BlobBase) # gm_headers/magick/error.h: 182

StreamEvent = (EventException + StreamBase) # gm_headers/magick/error.h: 182

CacheEvent = (EventException + CacheBase) # gm_headers/magick/error.h: 182

CoderEvent = (EventException + CoderBase) # gm_headers/magick/error.h: 182

ModuleEvent = (EventException + ModuleBase) # gm_headers/magick/error.h: 182

DrawEvent = (EventException + DrawBase) # gm_headers/magick/error.h: 182

RenderEvent = (EventException + RenderBase) # gm_headers/magick/error.h: 182

ImageEvent = (EventException + ImageBase) # gm_headers/magick/error.h: 182

WandEvent = (EventException + WandBase) # gm_headers/magick/error.h: 182

TemporaryFileEvent = (EventException + TemporaryFileBase) # gm_headers/magick/error.h: 182

TransformEvent = (EventException + TransformBase) # gm_headers/magick/error.h: 182

XServerEvent = (EventException + XServerBase) # gm_headers/magick/error.h: 182

X11Event = (EventException + X11Base) # gm_headers/magick/error.h: 182

UserEvent = (EventException + UserBase) # gm_headers/magick/error.h: 182

MonitorEvent = (EventException + MonitorBase) # gm_headers/magick/error.h: 182

LocaleEvent = (EventException + LocaleBase) # gm_headers/magick/error.h: 182

DeprecateEvent = (EventException + DeprecateBase) # gm_headers/magick/error.h: 182

RegistryEvent = (EventException + RegistryBase) # gm_headers/magick/error.h: 182

ConfigureEvent = (EventException + ConfigureBase) # gm_headers/magick/error.h: 182

WarningException = 300 # gm_headers/magick/error.h: 182

ExceptionWarning = (WarningException + ExceptionBase) # gm_headers/magick/error.h: 182

ResourceWarning = (WarningException + ResourceBase) # gm_headers/magick/error.h: 182

ResourceLimitWarning = (WarningException + ResourceLimitBase) # gm_headers/magick/error.h: 182

TypeWarning = (WarningException + TypeBase) # gm_headers/magick/error.h: 182

AnnotateWarning = (WarningException + AnnotateBase) # gm_headers/magick/error.h: 182

OptionWarning = (WarningException + OptionBase) # gm_headers/magick/error.h: 182

DelegateWarning = (WarningException + DelegateBase) # gm_headers/magick/error.h: 182

MissingDelegateWarning = (WarningException + MissingDelegateBase) # gm_headers/magick/error.h: 182

CorruptImageWarning = (WarningException + CorruptImageBase) # gm_headers/magick/error.h: 182

FileOpenWarning = (WarningException + FileOpenBase) # gm_headers/magick/error.h: 182

BlobWarning = (WarningException + BlobBase) # gm_headers/magick/error.h: 182

StreamWarning = (WarningException + StreamBase) # gm_headers/magick/error.h: 182

CacheWarning = (WarningException + CacheBase) # gm_headers/magick/error.h: 182

CoderWarning = (WarningException + CoderBase) # gm_headers/magick/error.h: 182

ModuleWarning = (WarningException + ModuleBase) # gm_headers/magick/error.h: 182

DrawWarning = (WarningException + DrawBase) # gm_headers/magick/error.h: 182

RenderWarning = (WarningException + RenderBase) # gm_headers/magick/error.h: 182

ImageWarning = (WarningException + ImageBase) # gm_headers/magick/error.h: 182

WandWarning = (WarningException + WandBase) # gm_headers/magick/error.h: 182

TemporaryFileWarning = (WarningException + TemporaryFileBase) # gm_headers/magick/error.h: 182

TransformWarning = (WarningException + TransformBase) # gm_headers/magick/error.h: 182

XServerWarning = (WarningException + XServerBase) # gm_headers/magick/error.h: 182

X11Warning = (WarningException + X11Base) # gm_headers/magick/error.h: 182

UserWarning = (WarningException + UserBase) # gm_headers/magick/error.h: 182

MonitorWarning = (WarningException + MonitorBase) # gm_headers/magick/error.h: 182

LocaleWarning = (WarningException + LocaleBase) # gm_headers/magick/error.h: 182

DeprecateWarning = (WarningException + DeprecateBase) # gm_headers/magick/error.h: 182

RegistryWarning = (WarningException + RegistryBase) # gm_headers/magick/error.h: 182

ConfigureWarning = (WarningException + ConfigureBase) # gm_headers/magick/error.h: 182

ErrorException = 400 # gm_headers/magick/error.h: 182

ExceptionError = (ErrorException + ExceptionBase) # gm_headers/magick/error.h: 182

ResourceError = (ErrorException + ResourceBase) # gm_headers/magick/error.h: 182

ResourceLimitError = (ErrorException + ResourceLimitBase) # gm_headers/magick/error.h: 182

TypeError = (ErrorException + TypeBase) # gm_headers/magick/error.h: 182

AnnotateError = (ErrorException + AnnotateBase) # gm_headers/magick/error.h: 182

OptionError = (ErrorException + OptionBase) # gm_headers/magick/error.h: 182

DelegateError = (ErrorException + DelegateBase) # gm_headers/magick/error.h: 182

MissingDelegateError = (ErrorException + MissingDelegateBase) # gm_headers/magick/error.h: 182

CorruptImageError = (ErrorException + CorruptImageBase) # gm_headers/magick/error.h: 182

FileOpenError = (ErrorException + FileOpenBase) # gm_headers/magick/error.h: 182

BlobError = (ErrorException + BlobBase) # gm_headers/magick/error.h: 182

StreamError = (ErrorException + StreamBase) # gm_headers/magick/error.h: 182

CacheError = (ErrorException + CacheBase) # gm_headers/magick/error.h: 182

CoderError = (ErrorException + CoderBase) # gm_headers/magick/error.h: 182

ModuleError = (ErrorException + ModuleBase) # gm_headers/magick/error.h: 182

DrawError = (ErrorException + DrawBase) # gm_headers/magick/error.h: 182

RenderError = (ErrorException + RenderBase) # gm_headers/magick/error.h: 182

ImageError = (ErrorException + ImageBase) # gm_headers/magick/error.h: 182

WandError = (ErrorException + WandBase) # gm_headers/magick/error.h: 182

TemporaryFileError = (ErrorException + TemporaryFileBase) # gm_headers/magick/error.h: 182

TransformError = (ErrorException + TransformBase) # gm_headers/magick/error.h: 182

XServerError = (ErrorException + XServerBase) # gm_headers/magick/error.h: 182

X11Error = (ErrorException + X11Base) # gm_headers/magick/error.h: 182

UserError = (ErrorException + UserBase) # gm_headers/magick/error.h: 182

MonitorError = (ErrorException + MonitorBase) # gm_headers/magick/error.h: 182

LocaleError = (ErrorException + LocaleBase) # gm_headers/magick/error.h: 182

DeprecateError = (ErrorException + DeprecateBase) # gm_headers/magick/error.h: 182

RegistryError = (ErrorException + RegistryBase) # gm_headers/magick/error.h: 182

ConfigureError = (ErrorException + ConfigureBase) # gm_headers/magick/error.h: 182

FatalErrorException = 700 # gm_headers/magick/error.h: 182

ExceptionFatalError = (FatalErrorException + ExceptionBase) # gm_headers/magick/error.h: 182

ResourceFatalError = (FatalErrorException + ResourceBase) # gm_headers/magick/error.h: 182

ResourceLimitFatalError = (FatalErrorException + ResourceLimitBase) # gm_headers/magick/error.h: 182

TypeFatalError = (FatalErrorException + TypeBase) # gm_headers/magick/error.h: 182

AnnotateFatalError = (FatalErrorException + AnnotateBase) # gm_headers/magick/error.h: 182

OptionFatalError = (FatalErrorException + OptionBase) # gm_headers/magick/error.h: 182

DelegateFatalError = (FatalErrorException + DelegateBase) # gm_headers/magick/error.h: 182

MissingDelegateFatalError = (FatalErrorException + MissingDelegateBase) # gm_headers/magick/error.h: 182

CorruptImageFatalError = (FatalErrorException + CorruptImageBase) # gm_headers/magick/error.h: 182

FileOpenFatalError = (FatalErrorException + FileOpenBase) # gm_headers/magick/error.h: 182

BlobFatalError = (FatalErrorException + BlobBase) # gm_headers/magick/error.h: 182

StreamFatalError = (FatalErrorException + StreamBase) # gm_headers/magick/error.h: 182

CacheFatalError = (FatalErrorException + CacheBase) # gm_headers/magick/error.h: 182

CoderFatalError = (FatalErrorException + CoderBase) # gm_headers/magick/error.h: 182

ModuleFatalError = (FatalErrorException + ModuleBase) # gm_headers/magick/error.h: 182

DrawFatalError = (FatalErrorException + DrawBase) # gm_headers/magick/error.h: 182

RenderFatalError = (FatalErrorException + RenderBase) # gm_headers/magick/error.h: 182

ImageFatalError = (FatalErrorException + ImageBase) # gm_headers/magick/error.h: 182

WandFatalError = (FatalErrorException + WandBase) # gm_headers/magick/error.h: 182

TemporaryFileFatalError = (FatalErrorException + TemporaryFileBase) # gm_headers/magick/error.h: 182

TransformFatalError = (FatalErrorException + TransformBase) # gm_headers/magick/error.h: 182

XServerFatalError = (FatalErrorException + XServerBase) # gm_headers/magick/error.h: 182

X11FatalError = (FatalErrorException + X11Base) # gm_headers/magick/error.h: 182

UserFatalError = (FatalErrorException + UserBase) # gm_headers/magick/error.h: 182

MonitorFatalError = (FatalErrorException + MonitorBase) # gm_headers/magick/error.h: 182

LocaleFatalError = (FatalErrorException + LocaleBase) # gm_headers/magick/error.h: 182

DeprecateFatalError = (FatalErrorException + DeprecateBase) # gm_headers/magick/error.h: 182

RegistryFatalError = (FatalErrorException + RegistryBase) # gm_headers/magick/error.h: 182

ConfigureFatalError = (FatalErrorException + ConfigureBase) # gm_headers/magick/error.h: 182

ExceptionType = enum_anon_7 # gm_headers/magick/error.h: 182

# gm_headers/magick/error.h: 226
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

ExceptionInfo = struct__ExceptionInfo # gm_headers/magick/error.h: 226

ErrorHandler = CFUNCTYPE(UNCHECKED(None), ExceptionType, String, String) # gm_headers/magick/error.h: 232

FatalErrorHandler = CFUNCTYPE(UNCHECKED(None), ExceptionType, String, String) # gm_headers/magick/error.h: 235

WarningHandler = CFUNCTYPE(UNCHECKED(None), ExceptionType, String, String) # gm_headers/magick/error.h: 238

# gm_headers/magick/error.h: 244
if hasattr(_libs['GraphicsMagick'], 'GetLocaleExceptionMessage'):
    GetLocaleExceptionMessage = _libs['GraphicsMagick'].GetLocaleExceptionMessage
    GetLocaleExceptionMessage.argtypes = [ExceptionType, String]
    if sizeof(c_int) == sizeof(c_void_p):
        GetLocaleExceptionMessage.restype = ReturnString
    else:
        GetLocaleExceptionMessage.restype = String
        GetLocaleExceptionMessage.errcheck = ReturnString

# gm_headers/magick/error.h: 244
if hasattr(_libs['GraphicsMagick'], 'GetLocaleMessage'):
    GetLocaleMessage = _libs['GraphicsMagick'].GetLocaleMessage
    GetLocaleMessage.argtypes = [String]
    if sizeof(c_int) == sizeof(c_void_p):
        GetLocaleMessage.restype = ReturnString
    else:
        GetLocaleMessage.restype = String
        GetLocaleMessage.errcheck = ReturnString

# gm_headers/magick/error.h: 248
if hasattr(_libs['GraphicsMagick'], 'SetErrorHandler'):
    SetErrorHandler = _libs['GraphicsMagick'].SetErrorHandler
    SetErrorHandler.argtypes = [ErrorHandler]
    SetErrorHandler.restype = ErrorHandler

# gm_headers/magick/error.h: 251
if hasattr(_libs['GraphicsMagick'], 'SetFatalErrorHandler'):
    SetFatalErrorHandler = _libs['GraphicsMagick'].SetFatalErrorHandler
    SetFatalErrorHandler.argtypes = [FatalErrorHandler]
    SetFatalErrorHandler.restype = FatalErrorHandler

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], 'CatchException'):
    CatchException = _libs['GraphicsMagick'].CatchException
    CatchException.argtypes = [POINTER(ExceptionInfo)]
    CatchException.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], 'CopyException'):
    CopyException = _libs['GraphicsMagick'].CopyException
    CopyException.argtypes = [POINTER(ExceptionInfo), POINTER(ExceptionInfo)]
    CopyException.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], 'DestroyExceptionInfo'):
    DestroyExceptionInfo = _libs['GraphicsMagick'].DestroyExceptionInfo
    DestroyExceptionInfo.argtypes = [POINTER(ExceptionInfo)]
    DestroyExceptionInfo.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], 'GetExceptionInfo'):
    GetExceptionInfo = _libs['GraphicsMagick'].GetExceptionInfo
    GetExceptionInfo.argtypes = [POINTER(ExceptionInfo)]
    GetExceptionInfo.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], 'MagickError'):
    MagickError = _libs['GraphicsMagick'].MagickError
    MagickError.argtypes = [ExceptionType, String, String]
    MagickError.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], 'MagickFatalError'):
    MagickFatalError = _libs['GraphicsMagick'].MagickFatalError
    MagickFatalError.argtypes = [ExceptionType, String, String]
    MagickFatalError.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], 'MagickWarning'):
    MagickWarning = _libs['GraphicsMagick'].MagickWarning
    MagickWarning.argtypes = [ExceptionType, String, String]
    MagickWarning.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], '_MagickError'):
    _MagickError = _libs['GraphicsMagick']._MagickError
    _MagickError.argtypes = [ExceptionType, String, String]
    _MagickError.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], '_MagickFatalError'):
    _MagickFatalError = _libs['GraphicsMagick']._MagickFatalError
    _MagickFatalError.argtypes = [ExceptionType, String, String]
    _MagickFatalError.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], '_MagickWarning'):
    _MagickWarning = _libs['GraphicsMagick']._MagickWarning
    _MagickWarning.argtypes = [ExceptionType, String, String]
    _MagickWarning.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], 'SetExceptionInfo'):
    SetExceptionInfo = _libs['GraphicsMagick'].SetExceptionInfo
    SetExceptionInfo.argtypes = [POINTER(ExceptionInfo), ExceptionType]
    SetExceptionInfo.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], 'ThrowException'):
    ThrowException = _libs['GraphicsMagick'].ThrowException
    ThrowException.argtypes = [POINTER(ExceptionInfo), ExceptionType, String, String]
    ThrowException.restype = None

# gm_headers/magick/error.h: 254
if hasattr(_libs['GraphicsMagick'], 'ThrowLoggedException'):
    ThrowLoggedException = _libs['GraphicsMagick'].ThrowLoggedException
    ThrowLoggedException.argtypes = [POINTER(ExceptionInfo), ExceptionType, String, String, String, String, c_ulong]
    ThrowLoggedException.restype = None

# gm_headers/magick/error.h: 271
if hasattr(_libs['GraphicsMagick'], 'SetWarningHandler'):
    SetWarningHandler = _libs['GraphicsMagick'].SetWarningHandler
    SetWarningHandler.argtypes = [WarningHandler]
    SetWarningHandler.restype = WarningHandler

enum_anon_9 = c_int # gm_headers/magick/colorspace.h: 110

ColorspaceType = enum_anon_9 # gm_headers/magick/colorspace.h: 110

enum_anon_10 = c_int # gm_headers/magick/timer.h: 26

TimerState = enum_anon_10 # gm_headers/magick/timer.h: 26

# gm_headers/magick/timer.h: 37
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

Timer = struct__Timer # gm_headers/magick/timer.h: 37

# gm_headers/magick/timer.h: 50
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

TimerInfo = struct__TimerInfo # gm_headers/magick/timer.h: 50

enum_anon_11 = c_int # /tmp/tmpu80Elu/image.h: 171

UnspecifiedAlpha = 0 # /tmp/tmpu80Elu/image.h: 171

AssociatedAlpha = (UnspecifiedAlpha + 1) # /tmp/tmpu80Elu/image.h: 171

UnassociatedAlpha = (AssociatedAlpha + 1) # /tmp/tmpu80Elu/image.h: 171

AlphaType = enum_anon_11 # /tmp/tmpu80Elu/image.h: 171

enum_anon_12 = c_int # /tmp/tmpu80Elu/image.h: 187

UndefinedChannel = 0 # /tmp/tmpu80Elu/image.h: 187

RedChannel = (UndefinedChannel + 1) # /tmp/tmpu80Elu/image.h: 187

CyanChannel = (RedChannel + 1) # /tmp/tmpu80Elu/image.h: 187

GreenChannel = (CyanChannel + 1) # /tmp/tmpu80Elu/image.h: 187

MagentaChannel = (GreenChannel + 1) # /tmp/tmpu80Elu/image.h: 187

BlueChannel = (MagentaChannel + 1) # /tmp/tmpu80Elu/image.h: 187

YellowChannel = (BlueChannel + 1) # /tmp/tmpu80Elu/image.h: 187

OpacityChannel = (YellowChannel + 1) # /tmp/tmpu80Elu/image.h: 187

BlackChannel = (OpacityChannel + 1) # /tmp/tmpu80Elu/image.h: 187

MatteChannel = (BlackChannel + 1) # /tmp/tmpu80Elu/image.h: 187

AllChannels = (MatteChannel + 1) # /tmp/tmpu80Elu/image.h: 187

GrayChannel = (AllChannels + 1) # /tmp/tmpu80Elu/image.h: 187

ChannelType = enum_anon_12 # /tmp/tmpu80Elu/image.h: 187

enum_anon_13 = c_int # /tmp/tmpu80Elu/image.h: 194

UndefinedClass = 0 # /tmp/tmpu80Elu/image.h: 194

DirectClass = (UndefinedClass + 1) # /tmp/tmpu80Elu/image.h: 194

PseudoClass = (DirectClass + 1) # /tmp/tmpu80Elu/image.h: 194

ClassType = enum_anon_13 # /tmp/tmpu80Elu/image.h: 194

enum_anon_14 = c_int # /tmp/tmpu80Elu/image.h: 235

UndefinedCompositeOp = 0 # /tmp/tmpu80Elu/image.h: 235

OverCompositeOp = (UndefinedCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

InCompositeOp = (OverCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

OutCompositeOp = (InCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

AtopCompositeOp = (OutCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

XorCompositeOp = (AtopCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

PlusCompositeOp = (XorCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

MinusCompositeOp = (PlusCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

AddCompositeOp = (MinusCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

SubtractCompositeOp = (AddCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

DifferenceCompositeOp = (SubtractCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

MultiplyCompositeOp = (DifferenceCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

BumpmapCompositeOp = (MultiplyCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

CopyCompositeOp = (BumpmapCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

CopyRedCompositeOp = (CopyCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

CopyGreenCompositeOp = (CopyRedCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

CopyBlueCompositeOp = (CopyGreenCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

CopyOpacityCompositeOp = (CopyBlueCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

ClearCompositeOp = (CopyOpacityCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

DissolveCompositeOp = (ClearCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

DisplaceCompositeOp = (DissolveCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

ModulateCompositeOp = (DisplaceCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

ThresholdCompositeOp = (ModulateCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

NoCompositeOp = (ThresholdCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

DarkenCompositeOp = (NoCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

LightenCompositeOp = (DarkenCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

HueCompositeOp = (LightenCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

SaturateCompositeOp = (HueCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

ColorizeCompositeOp = (SaturateCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

LuminizeCompositeOp = (ColorizeCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

ScreenCompositeOp = (LuminizeCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

OverlayCompositeOp = (ScreenCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

CopyCyanCompositeOp = (OverlayCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

CopyMagentaCompositeOp = (CopyCyanCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

CopyYellowCompositeOp = (CopyMagentaCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

CopyBlackCompositeOp = (CopyYellowCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

DivideCompositeOp = (CopyBlackCompositeOp + 1) # /tmp/tmpu80Elu/image.h: 235

CompositeOperator = enum_anon_14 # /tmp/tmpu80Elu/image.h: 235

enum_anon_15 = c_int # /tmp/tmpu80Elu/image.h: 249

UndefinedCompression = 0 # /tmp/tmpu80Elu/image.h: 249

NoCompression = (UndefinedCompression + 1) # /tmp/tmpu80Elu/image.h: 249

BZipCompression = (NoCompression + 1) # /tmp/tmpu80Elu/image.h: 249

FaxCompression = (BZipCompression + 1) # /tmp/tmpu80Elu/image.h: 249

Group4Compression = (FaxCompression + 1) # /tmp/tmpu80Elu/image.h: 249

JPEGCompression = (Group4Compression + 1) # /tmp/tmpu80Elu/image.h: 249

LosslessJPEGCompression = (JPEGCompression + 1) # /tmp/tmpu80Elu/image.h: 249

LZWCompression = (LosslessJPEGCompression + 1) # /tmp/tmpu80Elu/image.h: 249

RLECompression = (LZWCompression + 1) # /tmp/tmpu80Elu/image.h: 249

ZipCompression = (RLECompression + 1) # /tmp/tmpu80Elu/image.h: 249

CompressionType = enum_anon_15 # /tmp/tmpu80Elu/image.h: 249

enum_anon_16 = c_int # /tmp/tmpu80Elu/image.h: 257

UndefinedDispose = 0 # /tmp/tmpu80Elu/image.h: 257

NoneDispose = (UndefinedDispose + 1) # /tmp/tmpu80Elu/image.h: 257

BackgroundDispose = (NoneDispose + 1) # /tmp/tmpu80Elu/image.h: 257

PreviousDispose = (BackgroundDispose + 1) # /tmp/tmpu80Elu/image.h: 257

DisposeType = enum_anon_16 # /tmp/tmpu80Elu/image.h: 257

enum_anon_17 = c_int # /tmp/tmpu80Elu/image.h: 265

UndefinedEndian = 0 # /tmp/tmpu80Elu/image.h: 265

LSBEndian = (UndefinedEndian + 1) # /tmp/tmpu80Elu/image.h: 265

MSBEndian = (LSBEndian + 1) # /tmp/tmpu80Elu/image.h: 265

NativeEndian = (MSBEndian + 1) # /tmp/tmpu80Elu/image.h: 265

EndianType = enum_anon_17 # /tmp/tmpu80Elu/image.h: 265

enum_anon_18 = c_int # /tmp/tmpu80Elu/image.h: 285

UndefinedFilter = 0 # /tmp/tmpu80Elu/image.h: 285

PointFilter = (UndefinedFilter + 1) # /tmp/tmpu80Elu/image.h: 285

BoxFilter = (PointFilter + 1) # /tmp/tmpu80Elu/image.h: 285

TriangleFilter = (BoxFilter + 1) # /tmp/tmpu80Elu/image.h: 285

HermiteFilter = (TriangleFilter + 1) # /tmp/tmpu80Elu/image.h: 285

HanningFilter = (HermiteFilter + 1) # /tmp/tmpu80Elu/image.h: 285

HammingFilter = (HanningFilter + 1) # /tmp/tmpu80Elu/image.h: 285

BlackmanFilter = (HammingFilter + 1) # /tmp/tmpu80Elu/image.h: 285

GaussianFilter = (BlackmanFilter + 1) # /tmp/tmpu80Elu/image.h: 285

QuadraticFilter = (GaussianFilter + 1) # /tmp/tmpu80Elu/image.h: 285

CubicFilter = (QuadraticFilter + 1) # /tmp/tmpu80Elu/image.h: 285

CatromFilter = (CubicFilter + 1) # /tmp/tmpu80Elu/image.h: 285

MitchellFilter = (CatromFilter + 1) # /tmp/tmpu80Elu/image.h: 285

LanczosFilter = (MitchellFilter + 1) # /tmp/tmpu80Elu/image.h: 285

BesselFilter = (LanczosFilter + 1) # /tmp/tmpu80Elu/image.h: 285

SincFilter = (BesselFilter + 1) # /tmp/tmpu80Elu/image.h: 285

FilterTypes = enum_anon_18 # /tmp/tmpu80Elu/image.h: 285

enum_anon_19 = c_int # /tmp/tmpu80Elu/image.h: 311

NoValue = 0 # /tmp/tmpu80Elu/image.h: 311

XValue = 1 # /tmp/tmpu80Elu/image.h: 311

YValue = 2 # /tmp/tmpu80Elu/image.h: 311

WidthValue = 4 # /tmp/tmpu80Elu/image.h: 311

HeightValue = 8 # /tmp/tmpu80Elu/image.h: 311

AllValues = 15 # /tmp/tmpu80Elu/image.h: 311

XNegative = 16 # /tmp/tmpu80Elu/image.h: 311

YNegative = 32 # /tmp/tmpu80Elu/image.h: 311

PercentValue = 4096 # /tmp/tmpu80Elu/image.h: 311

AspectValue = 8192 # /tmp/tmpu80Elu/image.h: 311

LessValue = 16384 # /tmp/tmpu80Elu/image.h: 311

GreaterValue = 32768 # /tmp/tmpu80Elu/image.h: 311

AreaValue = 65536 # /tmp/tmpu80Elu/image.h: 311

MinimumValue = 131072 # /tmp/tmpu80Elu/image.h: 311

GeometryFlags = enum_anon_19 # /tmp/tmpu80Elu/image.h: 311

enum_anon_20 = c_int # /tmp/tmpu80Elu/image.h: 337

ForgetGravity = 0 # /tmp/tmpu80Elu/image.h: 337

NorthWestGravity = (ForgetGravity + 1) # /tmp/tmpu80Elu/image.h: 337

NorthGravity = (NorthWestGravity + 1) # /tmp/tmpu80Elu/image.h: 337

NorthEastGravity = (NorthGravity + 1) # /tmp/tmpu80Elu/image.h: 337

WestGravity = (NorthEastGravity + 1) # /tmp/tmpu80Elu/image.h: 337

CenterGravity = (WestGravity + 1) # /tmp/tmpu80Elu/image.h: 337

EastGravity = (CenterGravity + 1) # /tmp/tmpu80Elu/image.h: 337

SouthWestGravity = (EastGravity + 1) # /tmp/tmpu80Elu/image.h: 337

SouthGravity = (SouthWestGravity + 1) # /tmp/tmpu80Elu/image.h: 337

SouthEastGravity = (SouthGravity + 1) # /tmp/tmpu80Elu/image.h: 337

StaticGravity = (SouthEastGravity + 1) # /tmp/tmpu80Elu/image.h: 337

GravityType = enum_anon_20 # /tmp/tmpu80Elu/image.h: 337

enum_anon_21 = c_int # /tmp/tmpu80Elu/image.h: 352

UndefinedType = 0 # /tmp/tmpu80Elu/image.h: 352

BilevelType = (UndefinedType + 1) # /tmp/tmpu80Elu/image.h: 352

GrayscaleType = (BilevelType + 1) # /tmp/tmpu80Elu/image.h: 352

GrayscaleMatteType = (GrayscaleType + 1) # /tmp/tmpu80Elu/image.h: 352

PaletteType = (GrayscaleMatteType + 1) # /tmp/tmpu80Elu/image.h: 352

PaletteMatteType = (PaletteType + 1) # /tmp/tmpu80Elu/image.h: 352

TrueColorType = (PaletteMatteType + 1) # /tmp/tmpu80Elu/image.h: 352

TrueColorMatteType = (TrueColorType + 1) # /tmp/tmpu80Elu/image.h: 352

ColorSeparationType = (TrueColorMatteType + 1) # /tmp/tmpu80Elu/image.h: 352

ColorSeparationMatteType = (ColorSeparationType + 1) # /tmp/tmpu80Elu/image.h: 352

OptimizeType = (ColorSeparationMatteType + 1) # /tmp/tmpu80Elu/image.h: 352

ImageType = enum_anon_21 # /tmp/tmpu80Elu/image.h: 352

enum_anon_22 = c_int # /tmp/tmpu80Elu/image.h: 361

UndefinedInterlace = 0 # /tmp/tmpu80Elu/image.h: 361

NoInterlace = (UndefinedInterlace + 1) # /tmp/tmpu80Elu/image.h: 361

LineInterlace = (NoInterlace + 1) # /tmp/tmpu80Elu/image.h: 361

PlaneInterlace = (LineInterlace + 1) # /tmp/tmpu80Elu/image.h: 361

PartitionInterlace = (PlaneInterlace + 1) # /tmp/tmpu80Elu/image.h: 361

InterlaceType = enum_anon_22 # /tmp/tmpu80Elu/image.h: 361

enum_anon_23 = c_int # /tmp/tmpu80Elu/image.h: 369

UndefinedMode = 0 # /tmp/tmpu80Elu/image.h: 369

FrameMode = (UndefinedMode + 1) # /tmp/tmpu80Elu/image.h: 369

UnframeMode = (FrameMode + 1) # /tmp/tmpu80Elu/image.h: 369

ConcatenateMode = (UnframeMode + 1) # /tmp/tmpu80Elu/image.h: 369

MontageMode = enum_anon_23 # /tmp/tmpu80Elu/image.h: 369

enum_anon_24 = c_int # /tmp/tmpu80Elu/image.h: 379

UniformNoise = 0 # /tmp/tmpu80Elu/image.h: 379

GaussianNoise = (UniformNoise + 1) # /tmp/tmpu80Elu/image.h: 379

MultiplicativeGaussianNoise = (GaussianNoise + 1) # /tmp/tmpu80Elu/image.h: 379

ImpulseNoise = (MultiplicativeGaussianNoise + 1) # /tmp/tmpu80Elu/image.h: 379

LaplacianNoise = (ImpulseNoise + 1) # /tmp/tmpu80Elu/image.h: 379

PoissonNoise = (LaplacianNoise + 1) # /tmp/tmpu80Elu/image.h: 379

NoiseType = enum_anon_24 # /tmp/tmpu80Elu/image.h: 379

enum_anon_25 = c_int # /tmp/tmpu80Elu/image.h: 395

UndefinedOrientation = 0 # /tmp/tmpu80Elu/image.h: 395

TopLeftOrientation = (UndefinedOrientation + 1) # /tmp/tmpu80Elu/image.h: 395

TopRightOrientation = (TopLeftOrientation + 1) # /tmp/tmpu80Elu/image.h: 395

BottomRightOrientation = (TopRightOrientation + 1) # /tmp/tmpu80Elu/image.h: 395

BottomLeftOrientation = (BottomRightOrientation + 1) # /tmp/tmpu80Elu/image.h: 395

LeftTopOrientation = (BottomLeftOrientation + 1) # /tmp/tmpu80Elu/image.h: 395

RightTopOrientation = (LeftTopOrientation + 1) # /tmp/tmpu80Elu/image.h: 395

RightBottomOrientation = (RightTopOrientation + 1) # /tmp/tmpu80Elu/image.h: 395

LeftBottomOrientation = (RightBottomOrientation + 1) # /tmp/tmpu80Elu/image.h: 395

OrientationType = enum_anon_25 # /tmp/tmpu80Elu/image.h: 395

enum_anon_26 = c_int # /tmp/tmpu80Elu/image.h: 429

UndefinedPreview = 0 # /tmp/tmpu80Elu/image.h: 429

RotatePreview = (UndefinedPreview + 1) # /tmp/tmpu80Elu/image.h: 429

ShearPreview = (RotatePreview + 1) # /tmp/tmpu80Elu/image.h: 429

RollPreview = (ShearPreview + 1) # /tmp/tmpu80Elu/image.h: 429

HuePreview = (RollPreview + 1) # /tmp/tmpu80Elu/image.h: 429

SaturationPreview = (HuePreview + 1) # /tmp/tmpu80Elu/image.h: 429

BrightnessPreview = (SaturationPreview + 1) # /tmp/tmpu80Elu/image.h: 429

GammaPreview = (BrightnessPreview + 1) # /tmp/tmpu80Elu/image.h: 429

SpiffPreview = (GammaPreview + 1) # /tmp/tmpu80Elu/image.h: 429

DullPreview = (SpiffPreview + 1) # /tmp/tmpu80Elu/image.h: 429

GrayscalePreview = (DullPreview + 1) # /tmp/tmpu80Elu/image.h: 429

QuantizePreview = (GrayscalePreview + 1) # /tmp/tmpu80Elu/image.h: 429

DespecklePreview = (QuantizePreview + 1) # /tmp/tmpu80Elu/image.h: 429

ReduceNoisePreview = (DespecklePreview + 1) # /tmp/tmpu80Elu/image.h: 429

AddNoisePreview = (ReduceNoisePreview + 1) # /tmp/tmpu80Elu/image.h: 429

SharpenPreview = (AddNoisePreview + 1) # /tmp/tmpu80Elu/image.h: 429

BlurPreview = (SharpenPreview + 1) # /tmp/tmpu80Elu/image.h: 429

ThresholdPreview = (BlurPreview + 1) # /tmp/tmpu80Elu/image.h: 429

EdgeDetectPreview = (ThresholdPreview + 1) # /tmp/tmpu80Elu/image.h: 429

SpreadPreview = (EdgeDetectPreview + 1) # /tmp/tmpu80Elu/image.h: 429

SolarizePreview = (SpreadPreview + 1) # /tmp/tmpu80Elu/image.h: 429

ShadePreview = (SolarizePreview + 1) # /tmp/tmpu80Elu/image.h: 429

RaisePreview = (ShadePreview + 1) # /tmp/tmpu80Elu/image.h: 429

SegmentPreview = (RaisePreview + 1) # /tmp/tmpu80Elu/image.h: 429

SwirlPreview = (SegmentPreview + 1) # /tmp/tmpu80Elu/image.h: 429

ImplodePreview = (SwirlPreview + 1) # /tmp/tmpu80Elu/image.h: 429

WavePreview = (ImplodePreview + 1) # /tmp/tmpu80Elu/image.h: 429

OilPaintPreview = (WavePreview + 1) # /tmp/tmpu80Elu/image.h: 429

CharcoalDrawingPreview = (OilPaintPreview + 1) # /tmp/tmpu80Elu/image.h: 429

JPEGPreview = (CharcoalDrawingPreview + 1) # /tmp/tmpu80Elu/image.h: 429

PreviewType = enum_anon_26 # /tmp/tmpu80Elu/image.h: 429

enum_anon_27 = c_int # /tmp/tmpu80Elu/image.h: 438

UndefinedIntent = 0 # /tmp/tmpu80Elu/image.h: 438

SaturationIntent = (UndefinedIntent + 1) # /tmp/tmpu80Elu/image.h: 438

PerceptualIntent = (SaturationIntent + 1) # /tmp/tmpu80Elu/image.h: 438

AbsoluteIntent = (PerceptualIntent + 1) # /tmp/tmpu80Elu/image.h: 438

RelativeIntent = (AbsoluteIntent + 1) # /tmp/tmpu80Elu/image.h: 438

RenderingIntent = enum_anon_27 # /tmp/tmpu80Elu/image.h: 438

enum_anon_28 = c_int # /tmp/tmpu80Elu/image.h: 445

UndefinedResolution = 0 # /tmp/tmpu80Elu/image.h: 445

PixelsPerInchResolution = (UndefinedResolution + 1) # /tmp/tmpu80Elu/image.h: 445

PixelsPerCentimeterResolution = (PixelsPerInchResolution + 1) # /tmp/tmpu80Elu/image.h: 445

ResolutionType = enum_anon_28 # /tmp/tmpu80Elu/image.h: 445

# /tmp/tmpu80Elu/image.h: 459
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

AffineMatrix = struct__AffineMatrix # /tmp/tmpu80Elu/image.h: 459

# /tmp/tmpu80Elu/image.h: 467
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

PrimaryInfo = struct__PrimaryInfo # /tmp/tmpu80Elu/image.h: 467

# /tmp/tmpu80Elu/image.h: 476
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

ChromaticityInfo = struct__ChromaticityInfo # /tmp/tmpu80Elu/image.h: 476

# /tmp/tmpu80Elu/image.h: 534
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

PixelPacket = struct__PixelPacket # /tmp/tmpu80Elu/image.h: 534

# /tmp/tmpu80Elu/image.h: 543
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

DoublePixelPacket = struct__DoublePixelPacket # /tmp/tmpu80Elu/image.h: 543

# /tmp/tmpu80Elu/image.h: 555
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

ErrorInfo = struct__ErrorInfo # /tmp/tmpu80Elu/image.h: 555

# /tmp/tmpu80Elu/image.h: 568
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

FrameInfo = struct__FrameInfo # /tmp/tmpu80Elu/image.h: 568

IndexPacket = Quantum # /tmp/tmpu80Elu/image.h: 570

# /tmp/tmpu80Elu/image.h: 579
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

LongPixelPacket = struct__LongPixelPacket # /tmp/tmpu80Elu/image.h: 579

# /tmp/tmpu80Elu/image.h: 615
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

MontageInfo = struct__MontageInfo # /tmp/tmpu80Elu/image.h: 615

# /tmp/tmpu80Elu/image.h: 627
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

ProfileInfo = struct__ProfileInfo # /tmp/tmpu80Elu/image.h: 627

# /tmp/tmpu80Elu/image.h: 638
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

RectangleInfo = struct__RectangleInfo # /tmp/tmpu80Elu/image.h: 638

# /tmp/tmpu80Elu/image.h: 647
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

SegmentInfo = struct__SegmentInfo # /tmp/tmpu80Elu/image.h: 647

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

Image = struct__Image # /tmp/tmpu80Elu/image.h: 856

# /tmp/tmpu80Elu/image.h: 976
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

ImageInfo = struct__ImageInfo # /tmp/tmpu80Elu/image.h: 976

# /tmp/tmpu80Elu/image.h: 983
if hasattr(_libs['GraphicsMagick'], 'CatchImageException'):
    CatchImageException = _libs['GraphicsMagick'].CatchImageException
    CatchImageException.argtypes = [POINTER(Image)]
    CatchImageException.restype = ExceptionType

# /tmp/tmpu80Elu/image.h: 986
if hasattr(_libs['GraphicsMagick'], 'AllocateImage'):
    AllocateImage = _libs['GraphicsMagick'].AllocateImage
    AllocateImage.argtypes = [POINTER(ImageInfo)]
    AllocateImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/image.h: 986
if hasattr(_libs['GraphicsMagick'], 'AppendImages'):
    AppendImages = _libs['GraphicsMagick'].AppendImages
    AppendImages.argtypes = [POINTER(Image), c_uint, POINTER(ExceptionInfo)]
    AppendImages.restype = POINTER(Image)

# /tmp/tmpu80Elu/image.h: 986
if hasattr(_libs['GraphicsMagick'], 'CloneImage'):
    CloneImage = _libs['GraphicsMagick'].CloneImage
    CloneImage.argtypes = [POINTER(Image), c_ulong, c_ulong, c_uint, POINTER(ExceptionInfo)]
    CloneImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/image.h: 986
if hasattr(_libs['GraphicsMagick'], 'GetImageClipMask'):
    GetImageClipMask = _libs['GraphicsMagick'].GetImageClipMask
    GetImageClipMask.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    GetImageClipMask.restype = POINTER(Image)

# /tmp/tmpu80Elu/image.h: 986
if hasattr(_libs['GraphicsMagick'], 'ReferenceImage'):
    ReferenceImage = _libs['GraphicsMagick'].ReferenceImage
    ReferenceImage.argtypes = [POINTER(Image)]
    ReferenceImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/image.h: 994
if hasattr(_libs['GraphicsMagick'], 'CloneImageInfo'):
    CloneImageInfo = _libs['GraphicsMagick'].CloneImageInfo
    CloneImageInfo.argtypes = [POINTER(ImageInfo)]
    CloneImageInfo.restype = POINTER(ImageInfo)

# /tmp/tmpu80Elu/image.h: 997
if hasattr(_libs['GraphicsMagick'], 'AccessDefinition'):
    AccessDefinition = _libs['GraphicsMagick'].AccessDefinition
    AccessDefinition.argtypes = [POINTER(ImageInfo), String, String]
    if sizeof(c_int) == sizeof(c_void_p):
        AccessDefinition.restype = ReturnString
    else:
        AccessDefinition.restype = String
        AccessDefinition.errcheck = ReturnString

# /tmp/tmpu80Elu/image.h: 1001
if hasattr(_libs['GraphicsMagick'], 'GetImageGeometry'):
    GetImageGeometry = _libs['GraphicsMagick'].GetImageGeometry
    GetImageGeometry.argtypes = [POINTER(Image), String, c_uint, POINTER(RectangleInfo)]
    GetImageGeometry.restype = c_int

# /tmp/tmpu80Elu/image.h: 1006
if hasattr(_libs['GraphicsMagick'], 'IsTaintImage'):
    IsTaintImage = _libs['GraphicsMagick'].IsTaintImage
    IsTaintImage.argtypes = [POINTER(Image)]
    IsTaintImage.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1006
if hasattr(_libs['GraphicsMagick'], 'IsSubimage'):
    IsSubimage = _libs['GraphicsMagick'].IsSubimage
    IsSubimage.argtypes = [String, c_uint]
    IsSubimage.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'AddDefinitions'):
    AddDefinitions = _libs['GraphicsMagick'].AddDefinitions
    AddDefinitions.argtypes = [POINTER(ImageInfo), String, POINTER(ExceptionInfo)]
    AddDefinitions.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'AnimateImages'):
    AnimateImages = _libs['GraphicsMagick'].AnimateImages
    AnimateImages.argtypes = [POINTER(ImageInfo), POINTER(Image)]
    AnimateImages.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'ClipImage'):
    ClipImage = _libs['GraphicsMagick'].ClipImage
    ClipImage.argtypes = [POINTER(Image)]
    ClipImage.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'ClipPathImage'):
    ClipPathImage = _libs['GraphicsMagick'].ClipPathImage
    ClipPathImage.argtypes = [POINTER(Image), String, c_uint]
    ClipPathImage.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'DisplayImages'):
    DisplayImages = _libs['GraphicsMagick'].DisplayImages
    DisplayImages.argtypes = [POINTER(ImageInfo), POINTER(Image)]
    DisplayImages.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'RemoveDefinitions'):
    RemoveDefinitions = _libs['GraphicsMagick'].RemoveDefinitions
    RemoveDefinitions.argtypes = [POINTER(ImageInfo), String]
    RemoveDefinitions.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'SetImage'):
    SetImage = _libs['GraphicsMagick'].SetImage
    SetImage.argtypes = [POINTER(Image), Quantum]
    SetImage.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'SetImageClipMask'):
    SetImageClipMask = _libs['GraphicsMagick'].SetImageClipMask
    SetImageClipMask.argtypes = [POINTER(Image), POINTER(Image)]
    SetImageClipMask.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'SetImageDepth'):
    SetImageDepth = _libs['GraphicsMagick'].SetImageDepth
    SetImageDepth.argtypes = [POINTER(Image), c_ulong]
    SetImageDepth.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'SetImageInfo'):
    SetImageInfo = _libs['GraphicsMagick'].SetImageInfo
    SetImageInfo.argtypes = [POINTER(ImageInfo), c_uint, POINTER(ExceptionInfo)]
    SetImageInfo.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'SetImageType'):
    SetImageType = _libs['GraphicsMagick'].SetImageType
    SetImageType.argtypes = [POINTER(Image), ImageType]
    SetImageType.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1011
if hasattr(_libs['GraphicsMagick'], 'SyncImage'):
    SyncImage = _libs['GraphicsMagick'].SyncImage
    SyncImage.argtypes = [POINTER(Image)]
    SyncImage.restype = c_uint

# /tmp/tmpu80Elu/image.h: 1026
if hasattr(_libs['GraphicsMagick'], 'AllocateNextImage'):
    AllocateNextImage = _libs['GraphicsMagick'].AllocateNextImage
    AllocateNextImage.argtypes = [POINTER(ImageInfo), POINTER(Image)]
    AllocateNextImage.restype = None

# /tmp/tmpu80Elu/image.h: 1026
if hasattr(_libs['GraphicsMagick'], 'DestroyImage'):
    DestroyImage = _libs['GraphicsMagick'].DestroyImage
    DestroyImage.argtypes = [POINTER(Image)]
    DestroyImage.restype = None

# /tmp/tmpu80Elu/image.h: 1026
if hasattr(_libs['GraphicsMagick'], 'DestroyImageInfo'):
    DestroyImageInfo = _libs['GraphicsMagick'].DestroyImageInfo
    DestroyImageInfo.argtypes = [POINTER(ImageInfo)]
    DestroyImageInfo.restype = None

# /tmp/tmpu80Elu/image.h: 1026
if hasattr(_libs['GraphicsMagick'], 'GetImageException'):
    GetImageException = _libs['GraphicsMagick'].GetImageException
    GetImageException.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    GetImageException.restype = None

# /tmp/tmpu80Elu/image.h: 1026
if hasattr(_libs['GraphicsMagick'], 'GetImageInfo'):
    GetImageInfo = _libs['GraphicsMagick'].GetImageInfo
    GetImageInfo.argtypes = [POINTER(ImageInfo)]
    GetImageInfo.restype = None

# /tmp/tmpu80Elu/image.h: 1026
if hasattr(_libs['GraphicsMagick'], 'ModifyImage'):
    ModifyImage = _libs['GraphicsMagick'].ModifyImage
    ModifyImage.argtypes = [POINTER(POINTER(Image)), POINTER(ExceptionInfo)]
    ModifyImage.restype = None

# /tmp/tmpu80Elu/image.h: 1026
if hasattr(_libs['GraphicsMagick'], 'SetImageOpacity'):
    SetImageOpacity = _libs['GraphicsMagick'].SetImageOpacity
    SetImageOpacity.argtypes = [POINTER(Image), c_uint]
    SetImageOpacity.restype = None

DecoderHandler = CFUNCTYPE(UNCHECKED(POINTER(Image)), POINTER(ImageInfo), POINTER(ExceptionInfo)) # /tmp/tmpu80Elu/magick.h: 28

EncoderHandler = CFUNCTYPE(UNCHECKED(c_uint), POINTER(ImageInfo), POINTER(Image)) # /tmp/tmpu80Elu/magick.h: 31

MagickHandler = CFUNCTYPE(UNCHECKED(c_uint), POINTER(c_ubyte), c_size_t) # /tmp/tmpu80Elu/magick.h: 31

enum_anon_29 = c_int # /tmp/tmpu80Elu/magick.h: 42

UnstableCoderClass = 0 # /tmp/tmpu80Elu/magick.h: 42

StableCoderClass = (UnstableCoderClass + 1) # /tmp/tmpu80Elu/magick.h: 42

PrimaryCoderClass = (StableCoderClass + 1) # /tmp/tmpu80Elu/magick.h: 42

CoderClass = enum_anon_29 # /tmp/tmpu80Elu/magick.h: 42

enum_anon_30 = c_int # /tmp/tmpu80Elu/magick.h: 52

HintExtensionTreatment = 0 # /tmp/tmpu80Elu/magick.h: 52

ObeyExtensionTreatment = (HintExtensionTreatment + 1) # /tmp/tmpu80Elu/magick.h: 52

IgnoreExtensionTreatment = (ObeyExtensionTreatment + 1) # /tmp/tmpu80Elu/magick.h: 52

ExtensionTreatment = enum_anon_30 # /tmp/tmpu80Elu/magick.h: 52

# /tmp/tmpu80Elu/magick.h: 54
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

MagickInfo = struct__MagickInfo # /tmp/tmpu80Elu/magick.h: 103

# /tmp/tmpu80Elu/magick.h: 109
if hasattr(_libs['GraphicsMagick'], 'MagickToMime'):
    MagickToMime = _libs['GraphicsMagick'].MagickToMime
    MagickToMime.argtypes = [String]
    if sizeof(c_int) == sizeof(c_void_p):
        MagickToMime.restype = ReturnString
    else:
        MagickToMime.restype = String
        MagickToMime.errcheck = ReturnString

# /tmp/tmpu80Elu/magick.h: 112
if hasattr(_libs['GraphicsMagick'], 'GetImageMagick'):
    GetImageMagick = _libs['GraphicsMagick'].GetImageMagick
    GetImageMagick.argtypes = [POINTER(c_ubyte), c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        GetImageMagick.restype = ReturnString
    else:
        GetImageMagick.restype = String
        GetImageMagick.errcheck = ReturnString

# /tmp/tmpu80Elu/magick.h: 115
if hasattr(_libs['GraphicsMagick'], 'IsMagickConflict'):
    IsMagickConflict = _libs['GraphicsMagick'].IsMagickConflict
    IsMagickConflict.argtypes = [String]
    IsMagickConflict.restype = c_uint

# /tmp/tmpu80Elu/magick.h: 118
if hasattr(_libs['GraphicsMagick'], 'ListModuleMap'):
    ListModuleMap = _libs['GraphicsMagick'].ListModuleMap
    ListModuleMap.argtypes = [POINTER(FILE), POINTER(ExceptionInfo)]
    ListModuleMap.restype = c_uint

# /tmp/tmpu80Elu/magick.h: 118
if hasattr(_libs['GraphicsMagick'], 'ListMagickInfo'):
    ListMagickInfo = _libs['GraphicsMagick'].ListMagickInfo
    ListMagickInfo.argtypes = [POINTER(FILE), POINTER(ExceptionInfo)]
    ListMagickInfo.restype = c_uint

# /tmp/tmpu80Elu/magick.h: 118
if hasattr(_libs['GraphicsMagick'], 'UnregisterMagickInfo'):
    UnregisterMagickInfo = _libs['GraphicsMagick'].UnregisterMagickInfo
    UnregisterMagickInfo.argtypes = [String]
    UnregisterMagickInfo.restype = c_uint

# /tmp/tmpu80Elu/magick.h: 123
if hasattr(_libs['GraphicsMagick'], 'DestroyMagick'):
    DestroyMagick = _libs['GraphicsMagick'].DestroyMagick
    DestroyMagick.argtypes = []
    DestroyMagick.restype = None

# /tmp/tmpu80Elu/magick.h: 123
if hasattr(_libs['GraphicsMagick'], 'InitializeMagick'):
    InitializeMagick = _libs['GraphicsMagick'].InitializeMagick
    InitializeMagick.argtypes = [String]
    InitializeMagick.restype = None

# /tmp/tmpu80Elu/magick.h: 127
if hasattr(_libs['GraphicsMagick'], 'GetMagickInfo'):
    GetMagickInfo = _libs['GraphicsMagick'].GetMagickInfo
    GetMagickInfo.argtypes = [String, POINTER(ExceptionInfo)]
    GetMagickInfo.restype = POINTER(MagickInfo)

# /tmp/tmpu80Elu/magick.h: 130
if hasattr(_libs['GraphicsMagick'], 'GetMagickInfoArray'):
    GetMagickInfoArray = _libs['GraphicsMagick'].GetMagickInfoArray
    GetMagickInfoArray.argtypes = [POINTER(ExceptionInfo)]
    GetMagickInfoArray.restype = POINTER(POINTER(MagickInfo))

# /tmp/tmpu80Elu/magick.h: 133
if hasattr(_libs['GraphicsMagick'], 'RegisterMagickInfo'):
    RegisterMagickInfo = _libs['GraphicsMagick'].RegisterMagickInfo
    RegisterMagickInfo.argtypes = [POINTER(MagickInfo)]
    RegisterMagickInfo.restype = POINTER(MagickInfo)

# /tmp/tmpu80Elu/magick.h: 133
if hasattr(_libs['GraphicsMagick'], 'SetMagickInfo'):
    SetMagickInfo = _libs['GraphicsMagick'].SetMagickInfo
    SetMagickInfo.argtypes = [String]
    SetMagickInfo.restype = POINTER(MagickInfo)

enum_anon_31 = c_int # /tmp/tmpu80Elu/constitute.h: 54

UndefinedQuantum = 0 # /tmp/tmpu80Elu/constitute.h: 54

IndexQuantum = (UndefinedQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

GrayQuantum = (IndexQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

IndexAlphaQuantum = (GrayQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

GrayAlphaQuantum = (IndexAlphaQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

RedQuantum = (GrayAlphaQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

CyanQuantum = (RedQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

GreenQuantum = (CyanQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

YellowQuantum = (GreenQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

BlueQuantum = (YellowQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

MagentaQuantum = (BlueQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

AlphaQuantum = (MagentaQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

BlackQuantum = (AlphaQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

RGBQuantum = (BlackQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

RGBAQuantum = (RGBQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

CMYKQuantum = (RGBAQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

CMYKAQuantum = (CMYKQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

CIEYQuantum = (CMYKAQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

CIEXYZQuantum = (CIEYQuantum + 1) # /tmp/tmpu80Elu/constitute.h: 54

QuantumType = enum_anon_31 # /tmp/tmpu80Elu/constitute.h: 54

enum_anon_32 = c_int # /tmp/tmpu80Elu/constitute.h: 64

UndefinedQuantumSampleType = 0 # /tmp/tmpu80Elu/constitute.h: 64

UnsignedQuantumSampleType = (UndefinedQuantumSampleType + 1) # /tmp/tmpu80Elu/constitute.h: 64

FloatQuantumSampleType = (UnsignedQuantumSampleType + 1) # /tmp/tmpu80Elu/constitute.h: 64

QuantumSampleType = enum_anon_32 # /tmp/tmpu80Elu/constitute.h: 64

enum_anon_33 = c_int # /tmp/tmpu80Elu/constitute.h: 77

CharPixel = 0 # /tmp/tmpu80Elu/constitute.h: 77

ShortPixel = (CharPixel + 1) # /tmp/tmpu80Elu/constitute.h: 77

IntegerPixel = (ShortPixel + 1) # /tmp/tmpu80Elu/constitute.h: 77

LongPixel = (IntegerPixel + 1) # /tmp/tmpu80Elu/constitute.h: 77

FloatPixel = (LongPixel + 1) # /tmp/tmpu80Elu/constitute.h: 77

DoublePixel = (FloatPixel + 1) # /tmp/tmpu80Elu/constitute.h: 77

StorageType = enum_anon_33 # /tmp/tmpu80Elu/constitute.h: 77

# /tmp/tmpu80Elu/constitute.h: 105
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

ExportPixelAreaOptions = struct__ExportPixelAreaOptions # /tmp/tmpu80Elu/constitute.h: 105

# /tmp/tmpu80Elu/constitute.h: 115
class struct__ExportPixelAreaInfo(Structure):
    pass

struct__ExportPixelAreaInfo.__slots__ = [
    'bytes_exported',
]
struct__ExportPixelAreaInfo._fields_ = [
    ('bytes_exported', c_size_t),
]

ExportPixelAreaInfo = struct__ExportPixelAreaInfo # /tmp/tmpu80Elu/constitute.h: 115

# /tmp/tmpu80Elu/constitute.h: 137
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

ImportPixelAreaOptions = struct__ImportPixelAreaOptions # /tmp/tmpu80Elu/constitute.h: 137

# /tmp/tmpu80Elu/constitute.h: 147
class struct__ImportPixelAreaInfo(Structure):
    pass

struct__ImportPixelAreaInfo.__slots__ = [
    'bytes_imported',
]
struct__ImportPixelAreaInfo._fields_ = [
    ('bytes_imported', c_size_t),
]

ImportPixelAreaInfo = struct__ImportPixelAreaInfo # /tmp/tmpu80Elu/constitute.h: 147

# /tmp/tmpu80Elu/constitute.h: 150
if hasattr(_libs['GraphicsMagick'], 'StorageTypeToString'):
    StorageTypeToString = _libs['GraphicsMagick'].StorageTypeToString
    StorageTypeToString.argtypes = [StorageType]
    if sizeof(c_int) == sizeof(c_void_p):
        StorageTypeToString.restype = ReturnString
    else:
        StorageTypeToString.restype = String
        StorageTypeToString.errcheck = ReturnString

# /tmp/tmpu80Elu/constitute.h: 150
if hasattr(_libs['GraphicsMagick'], 'QuantumSampleTypeToString'):
    QuantumSampleTypeToString = _libs['GraphicsMagick'].QuantumSampleTypeToString
    QuantumSampleTypeToString.argtypes = [QuantumSampleType]
    if sizeof(c_int) == sizeof(c_void_p):
        QuantumSampleTypeToString.restype = ReturnString
    else:
        QuantumSampleTypeToString.restype = String
        QuantumSampleTypeToString.errcheck = ReturnString

# /tmp/tmpu80Elu/constitute.h: 150
if hasattr(_libs['GraphicsMagick'], 'QuantumTypeToString'):
    QuantumTypeToString = _libs['GraphicsMagick'].QuantumTypeToString
    QuantumTypeToString.argtypes = [QuantumType]
    if sizeof(c_int) == sizeof(c_void_p):
        QuantumTypeToString.restype = ReturnString
    else:
        QuantumTypeToString.restype = String
        QuantumTypeToString.errcheck = ReturnString

# /tmp/tmpu80Elu/constitute.h: 155
if hasattr(_libs['GraphicsMagick'], 'ConstituteImage'):
    ConstituteImage = _libs['GraphicsMagick'].ConstituteImage
    ConstituteImage.argtypes = [c_ulong, c_ulong, String, StorageType, POINTER(None), POINTER(ExceptionInfo)]
    ConstituteImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/constitute.h: 155
if hasattr(_libs['GraphicsMagick'], 'ConstituteTextureImage'):
    ConstituteTextureImage = _libs['GraphicsMagick'].ConstituteTextureImage
    ConstituteTextureImage.argtypes = [c_ulong, c_ulong, POINTER(Image), POINTER(ExceptionInfo)]
    ConstituteTextureImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/constitute.h: 155
if hasattr(_libs['GraphicsMagick'], 'PingImage'):
    PingImage = _libs['GraphicsMagick'].PingImage
    PingImage.argtypes = [POINTER(ImageInfo), POINTER(ExceptionInfo)]
    PingImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/constitute.h: 155
if hasattr(_libs['GraphicsMagick'], 'ReadImage'):
    ReadImage = _libs['GraphicsMagick'].ReadImage
    ReadImage.argtypes = [POINTER(ImageInfo), POINTER(ExceptionInfo)]
    ReadImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/constitute.h: 155
if hasattr(_libs['GraphicsMagick'], 'ReadInlineImage'):
    ReadInlineImage = _libs['GraphicsMagick'].ReadInlineImage
    ReadInlineImage.argtypes = [POINTER(ImageInfo), String, POINTER(ExceptionInfo)]
    ReadInlineImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/constitute.h: 166
if hasattr(_libs['GraphicsMagick'], 'DispatchImage'):
    DispatchImage = _libs['GraphicsMagick'].DispatchImage
    DispatchImage.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong, String, StorageType, POINTER(None), POINTER(ExceptionInfo)]
    DispatchImage.restype = c_uint

# /tmp/tmpu80Elu/constitute.h: 166
if hasattr(_libs['GraphicsMagick'], 'ExportImagePixelArea'):
    ExportImagePixelArea = _libs['GraphicsMagick'].ExportImagePixelArea
    ExportImagePixelArea.argtypes = [POINTER(Image), QuantumType, c_uint, POINTER(c_ubyte), POINTER(ExportPixelAreaOptions), POINTER(ExportPixelAreaInfo)]
    ExportImagePixelArea.restype = c_uint

# /tmp/tmpu80Elu/constitute.h: 166
if hasattr(_libs['GraphicsMagick'], 'ExportViewPixelArea'):
    ExportViewPixelArea = _libs['GraphicsMagick'].ExportViewPixelArea
    ExportViewPixelArea.argtypes = [POINTER(ViewInfo), QuantumType, c_uint, POINTER(c_ubyte), POINTER(ExportPixelAreaOptions), POINTER(ExportPixelAreaInfo)]
    ExportViewPixelArea.restype = c_uint

# /tmp/tmpu80Elu/constitute.h: 177
if hasattr(_libs['GraphicsMagick'], 'ImportImagePixelArea'):
    ImportImagePixelArea = _libs['GraphicsMagick'].ImportImagePixelArea
    ImportImagePixelArea.argtypes = [POINTER(Image), QuantumType, c_uint, POINTER(c_ubyte), POINTER(ImportPixelAreaOptions), POINTER(ImportPixelAreaInfo)]
    ImportImagePixelArea.restype = c_uint

# /tmp/tmpu80Elu/constitute.h: 177
if hasattr(_libs['GraphicsMagick'], 'ImportViewPixelArea'):
    ImportViewPixelArea = _libs['GraphicsMagick'].ImportViewPixelArea
    ImportViewPixelArea.argtypes = [POINTER(ViewInfo), QuantumType, c_uint, POINTER(c_ubyte), POINTER(ImportPixelAreaOptions), POINTER(ImportPixelAreaInfo)]
    ImportViewPixelArea.restype = c_uint

# /tmp/tmpu80Elu/constitute.h: 177
if hasattr(_libs['GraphicsMagick'], 'WriteImage'):
    WriteImage = _libs['GraphicsMagick'].WriteImage
    WriteImage.argtypes = [POINTER(ImageInfo), POINTER(Image)]
    WriteImage.restype = c_uint

# /tmp/tmpu80Elu/constitute.h: 177
if hasattr(_libs['GraphicsMagick'], 'WriteImages'):
    WriteImages = _libs['GraphicsMagick'].WriteImages
    WriteImages.argtypes = [POINTER(ImageInfo), POINTER(Image), String, POINTER(ExceptionInfo)]
    WriteImages.restype = c_uint

# /tmp/tmpu80Elu/constitute.h: 188
if hasattr(_libs['GraphicsMagick'], 'ExportPixelAreaOptionsInit'):
    ExportPixelAreaOptionsInit = _libs['GraphicsMagick'].ExportPixelAreaOptionsInit
    ExportPixelAreaOptionsInit.argtypes = [POINTER(ExportPixelAreaOptions)]
    ExportPixelAreaOptionsInit.restype = None

# /tmp/tmpu80Elu/constitute.h: 188
if hasattr(_libs['GraphicsMagick'], 'ImportPixelAreaOptionsInit'):
    ImportPixelAreaOptionsInit = _libs['GraphicsMagick'].ImportPixelAreaOptionsInit
    ImportPixelAreaOptionsInit.argtypes = [POINTER(ImportPixelAreaOptions)]
    ImportPixelAreaOptionsInit.restype = None

# /tmp/tmpu80Elu/constitute.h: 192
if hasattr(_libs['GraphicsMagick'], 'MagickFindRawImageMinMax'):
    MagickFindRawImageMinMax = _libs['GraphicsMagick'].MagickFindRawImageMinMax
    MagickFindRawImageMinMax.argtypes = [POINTER(Image), EndianType, c_ulong, c_ulong, StorageType, c_uint, POINTER(None), POINTER(c_double), POINTER(c_double)]
    MagickFindRawImageMinMax.restype = c_uint

# /tmp/tmpu80Elu/resize.h: 29
if hasattr(_libs['GraphicsMagick'], 'MagnifyImage'):
    MagnifyImage = _libs['GraphicsMagick'].MagnifyImage
    MagnifyImage.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    MagnifyImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/resize.h: 29
if hasattr(_libs['GraphicsMagick'], 'MinifyImage'):
    MinifyImage = _libs['GraphicsMagick'].MinifyImage
    MinifyImage.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    MinifyImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/resize.h: 29
if hasattr(_libs['GraphicsMagick'], 'ResizeImage'):
    ResizeImage = _libs['GraphicsMagick'].ResizeImage
    ResizeImage.argtypes = [POINTER(Image), c_ulong, c_ulong, FilterTypes, c_double, POINTER(ExceptionInfo)]
    ResizeImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/resize.h: 29
if hasattr(_libs['GraphicsMagick'], 'SampleImage'):
    SampleImage = _libs['GraphicsMagick'].SampleImage
    SampleImage.argtypes = [POINTER(Image), c_ulong, c_ulong, POINTER(ExceptionInfo)]
    SampleImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/resize.h: 29
if hasattr(_libs['GraphicsMagick'], 'ScaleImage'):
    ScaleImage = _libs['GraphicsMagick'].ScaleImage
    ScaleImage.argtypes = [POINTER(Image), c_ulong, c_ulong, POINTER(ExceptionInfo)]
    ScaleImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/resize.h: 29
if hasattr(_libs['GraphicsMagick'], 'ThumbnailImage'):
    ThumbnailImage = _libs['GraphicsMagick'].ThumbnailImage
    ThumbnailImage.argtypes = [POINTER(Image), c_ulong, c_ulong, POINTER(ExceptionInfo)]
    ThumbnailImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/resize.h: 29
if hasattr(_libs['GraphicsMagick'], 'ZoomImage'):
    ZoomImage = _libs['GraphicsMagick'].ZoomImage
    ZoomImage.argtypes = [POINTER(Image), c_ulong, c_ulong, POINTER(ExceptionInfo)]
    ZoomImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/delegate.h: 29
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

DelegateInfo = struct__DelegateInfo # /tmp/tmpu80Elu/delegate.h: 50

# /tmp/tmpu80Elu/delegate.h: 56
if hasattr(_libs['GraphicsMagick'], 'GetDelegateCommand'):
    GetDelegateCommand = _libs['GraphicsMagick'].GetDelegateCommand
    GetDelegateCommand.argtypes = [POINTER(ImageInfo), POINTER(Image), String, String, POINTER(ExceptionInfo)]
    if sizeof(c_int) == sizeof(c_void_p):
        GetDelegateCommand.restype = ReturnString
    else:
        GetDelegateCommand.restype = String
        GetDelegateCommand.errcheck = ReturnString

# /tmp/tmpu80Elu/delegate.h: 61
if hasattr(_libs['GraphicsMagick'], 'GetDelegateInfo'):
    GetDelegateInfo = _libs['GraphicsMagick'].GetDelegateInfo
    GetDelegateInfo.argtypes = [String, String, POINTER(ExceptionInfo)]
    GetDelegateInfo.restype = POINTER(DelegateInfo)

# /tmp/tmpu80Elu/delegate.h: 61
if hasattr(_libs['GraphicsMagick'], 'GetPostscriptDelegateInfo'):
    GetPostscriptDelegateInfo = _libs['GraphicsMagick'].GetPostscriptDelegateInfo
    GetPostscriptDelegateInfo.argtypes = [POINTER(ImageInfo), POINTER(c_uint), POINTER(ExceptionInfo)]
    GetPostscriptDelegateInfo.restype = POINTER(DelegateInfo)

# /tmp/tmpu80Elu/delegate.h: 67
if hasattr(_libs['GraphicsMagick'], 'SetDelegateInfo'):
    SetDelegateInfo = _libs['GraphicsMagick'].SetDelegateInfo
    SetDelegateInfo.argtypes = [POINTER(DelegateInfo)]
    SetDelegateInfo.restype = POINTER(DelegateInfo)

# /tmp/tmpu80Elu/delegate.h: 70
if hasattr(_libs['GraphicsMagick'], 'InvokePostscriptDelegate'):
    InvokePostscriptDelegate = _libs['GraphicsMagick'].InvokePostscriptDelegate
    InvokePostscriptDelegate.argtypes = [c_uint, String, POINTER(ExceptionInfo)]
    InvokePostscriptDelegate.restype = c_uint

# /tmp/tmpu80Elu/delegate.h: 70
if hasattr(_libs['GraphicsMagick'], 'InvokeDelegate'):
    InvokeDelegate = _libs['GraphicsMagick'].InvokeDelegate
    InvokeDelegate.argtypes = [POINTER(ImageInfo), POINTER(Image), String, String, POINTER(ExceptionInfo)]
    InvokeDelegate.restype = c_uint

# /tmp/tmpu80Elu/delegate.h: 70
if hasattr(_libs['GraphicsMagick'], 'ListDelegateInfo'):
    ListDelegateInfo = _libs['GraphicsMagick'].ListDelegateInfo
    ListDelegateInfo.argtypes = [POINTER(FILE), POINTER(ExceptionInfo)]
    ListDelegateInfo.restype = c_uint

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'AdaptiveThresholdImage'):
    AdaptiveThresholdImage = _libs['GraphicsMagick'].AdaptiveThresholdImage
    AdaptiveThresholdImage.argtypes = [POINTER(Image), c_ulong, c_ulong, c_double, POINTER(ExceptionInfo)]
    AdaptiveThresholdImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'AddNoiseImage'):
    AddNoiseImage = _libs['GraphicsMagick'].AddNoiseImage
    AddNoiseImage.argtypes = [POINTER(Image), NoiseType, POINTER(ExceptionInfo)]
    AddNoiseImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'AddNoiseImageChannel'):
    AddNoiseImageChannel = _libs['GraphicsMagick'].AddNoiseImageChannel
    AddNoiseImageChannel.argtypes = [POINTER(Image), ChannelType, NoiseType, POINTER(ExceptionInfo)]
    AddNoiseImageChannel.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'BlurImage'):
    BlurImage = _libs['GraphicsMagick'].BlurImage
    BlurImage.argtypes = [POINTER(Image), c_double, c_double, POINTER(ExceptionInfo)]
    BlurImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'BlurImageChannel'):
    BlurImageChannel = _libs['GraphicsMagick'].BlurImageChannel
    BlurImageChannel.argtypes = [POINTER(Image), ChannelType, c_double, c_double, POINTER(ExceptionInfo)]
    BlurImageChannel.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'ConvolveImage'):
    ConvolveImage = _libs['GraphicsMagick'].ConvolveImage
    ConvolveImage.argtypes = [POINTER(Image), c_uint, POINTER(c_double), POINTER(ExceptionInfo)]
    ConvolveImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'DespeckleImage'):
    DespeckleImage = _libs['GraphicsMagick'].DespeckleImage
    DespeckleImage.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    DespeckleImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'EdgeImage'):
    EdgeImage = _libs['GraphicsMagick'].EdgeImage
    EdgeImage.argtypes = [POINTER(Image), c_double, POINTER(ExceptionInfo)]
    EdgeImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'EmbossImage'):
    EmbossImage = _libs['GraphicsMagick'].EmbossImage
    EmbossImage.argtypes = [POINTER(Image), c_double, c_double, POINTER(ExceptionInfo)]
    EmbossImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'EnhanceImage'):
    EnhanceImage = _libs['GraphicsMagick'].EnhanceImage
    EnhanceImage.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    EnhanceImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'GaussianBlurImage'):
    GaussianBlurImage = _libs['GraphicsMagick'].GaussianBlurImage
    GaussianBlurImage.argtypes = [POINTER(Image), c_double, c_double, POINTER(ExceptionInfo)]
    GaussianBlurImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'GaussianBlurImageChannel'):
    GaussianBlurImageChannel = _libs['GraphicsMagick'].GaussianBlurImageChannel
    GaussianBlurImageChannel.argtypes = [POINTER(Image), ChannelType, c_double, c_double, POINTER(ExceptionInfo)]
    GaussianBlurImageChannel.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'MedianFilterImage'):
    MedianFilterImage = _libs['GraphicsMagick'].MedianFilterImage
    MedianFilterImage.argtypes = [POINTER(Image), c_double, POINTER(ExceptionInfo)]
    MedianFilterImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'MotionBlurImage'):
    MotionBlurImage = _libs['GraphicsMagick'].MotionBlurImage
    MotionBlurImage.argtypes = [POINTER(Image), c_double, c_double, c_double, POINTER(ExceptionInfo)]
    MotionBlurImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'ReduceNoiseImage'):
    ReduceNoiseImage = _libs['GraphicsMagick'].ReduceNoiseImage
    ReduceNoiseImage.argtypes = [POINTER(Image), c_double, POINTER(ExceptionInfo)]
    ReduceNoiseImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'ShadeImage'):
    ShadeImage = _libs['GraphicsMagick'].ShadeImage
    ShadeImage.argtypes = [POINTER(Image), c_uint, c_double, c_double, POINTER(ExceptionInfo)]
    ShadeImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'SharpenImage'):
    SharpenImage = _libs['GraphicsMagick'].SharpenImage
    SharpenImage.argtypes = [POINTER(Image), c_double, c_double, POINTER(ExceptionInfo)]
    SharpenImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'SharpenImageChannel'):
    SharpenImageChannel = _libs['GraphicsMagick'].SharpenImageChannel
    SharpenImageChannel.argtypes = [POINTER(Image), ChannelType, c_double, c_double, POINTER(ExceptionInfo)]
    SharpenImageChannel.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'SpreadImage'):
    SpreadImage = _libs['GraphicsMagick'].SpreadImage
    SpreadImage.argtypes = [POINTER(Image), c_uint, POINTER(ExceptionInfo)]
    SpreadImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'UnsharpMaskImage'):
    UnsharpMaskImage = _libs['GraphicsMagick'].UnsharpMaskImage
    UnsharpMaskImage.argtypes = [POINTER(Image), c_double, c_double, c_double, c_double, POINTER(ExceptionInfo)]
    UnsharpMaskImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 27
if hasattr(_libs['GraphicsMagick'], 'UnsharpMaskImageChannel'):
    UnsharpMaskImageChannel = _libs['GraphicsMagick'].UnsharpMaskImageChannel
    UnsharpMaskImageChannel.argtypes = [POINTER(Image), ChannelType, c_double, c_double, c_double, c_double, POINTER(ExceptionInfo)]
    UnsharpMaskImageChannel.restype = POINTER(Image)

# /tmp/tmpu80Elu/effect.h: 62
if hasattr(_libs['GraphicsMagick'], 'BlackThresholdImage'):
    BlackThresholdImage = _libs['GraphicsMagick'].BlackThresholdImage
    BlackThresholdImage.argtypes = [POINTER(Image), String]
    BlackThresholdImage.restype = c_uint

# /tmp/tmpu80Elu/effect.h: 62
if hasattr(_libs['GraphicsMagick'], 'ChannelThresholdImage'):
    ChannelThresholdImage = _libs['GraphicsMagick'].ChannelThresholdImage
    ChannelThresholdImage.argtypes = [POINTER(Image), String]
    ChannelThresholdImage.restype = c_uint

# /tmp/tmpu80Elu/effect.h: 62
if hasattr(_libs['GraphicsMagick'], 'RandomChannelThresholdImage'):
    RandomChannelThresholdImage = _libs['GraphicsMagick'].RandomChannelThresholdImage
    RandomChannelThresholdImage.argtypes = [POINTER(Image), String, String, POINTER(ExceptionInfo)]
    RandomChannelThresholdImage.restype = c_uint

# /tmp/tmpu80Elu/effect.h: 62
if hasattr(_libs['GraphicsMagick'], 'ThresholdImage'):
    ThresholdImage = _libs['GraphicsMagick'].ThresholdImage
    ThresholdImage.argtypes = [POINTER(Image), c_double]
    ThresholdImage.restype = c_uint

# /tmp/tmpu80Elu/effect.h: 62
if hasattr(_libs['GraphicsMagick'], 'WhiteThresholdImage'):
    WhiteThresholdImage = _libs['GraphicsMagick'].WhiteThresholdImage
    WhiteThresholdImage.argtypes = [POINTER(Image), String]
    WhiteThresholdImage.restype = c_uint

# /tmp/tmpu80Elu/enhance.h: 27
if hasattr(_libs['GraphicsMagick'], 'ContrastImage'):
    ContrastImage = _libs['GraphicsMagick'].ContrastImage
    ContrastImage.argtypes = [POINTER(Image), c_uint]
    ContrastImage.restype = c_uint

# /tmp/tmpu80Elu/enhance.h: 27
if hasattr(_libs['GraphicsMagick'], 'EqualizeImage'):
    EqualizeImage = _libs['GraphicsMagick'].EqualizeImage
    EqualizeImage.argtypes = [POINTER(Image)]
    EqualizeImage.restype = c_uint

# /tmp/tmpu80Elu/enhance.h: 27
if hasattr(_libs['GraphicsMagick'], 'GammaImage'):
    GammaImage = _libs['GraphicsMagick'].GammaImage
    GammaImage.argtypes = [POINTER(Image), String]
    GammaImage.restype = c_uint

# /tmp/tmpu80Elu/enhance.h: 27
if hasattr(_libs['GraphicsMagick'], 'LevelImage'):
    LevelImage = _libs['GraphicsMagick'].LevelImage
    LevelImage.argtypes = [POINTER(Image), String]
    LevelImage.restype = c_uint

# /tmp/tmpu80Elu/enhance.h: 27
if hasattr(_libs['GraphicsMagick'], 'LevelImageChannel'):
    LevelImageChannel = _libs['GraphicsMagick'].LevelImageChannel
    LevelImageChannel.argtypes = [POINTER(Image), ChannelType, c_double, c_double, c_double]
    LevelImageChannel.restype = c_uint

# /tmp/tmpu80Elu/enhance.h: 27
if hasattr(_libs['GraphicsMagick'], 'ModulateImage'):
    ModulateImage = _libs['GraphicsMagick'].ModulateImage
    ModulateImage.argtypes = [POINTER(Image), String]
    ModulateImage.restype = c_uint

# /tmp/tmpu80Elu/enhance.h: 27
if hasattr(_libs['GraphicsMagick'], 'NegateImage'):
    NegateImage = _libs['GraphicsMagick'].NegateImage
    NegateImage.argtypes = [POINTER(Image), c_uint]
    NegateImage.restype = c_uint

# /tmp/tmpu80Elu/enhance.h: 27
if hasattr(_libs['GraphicsMagick'], 'NormalizeImage'):
    NormalizeImage = _libs['GraphicsMagick'].NormalizeImage
    NormalizeImage.argtypes = [POINTER(Image)]
    NormalizeImage.restype = c_uint

enum_anon_34 = c_int # /tmp/tmpu80Elu/pixel_cache.h: 39

UndefinedVirtualPixelMethod = 0 # /tmp/tmpu80Elu/pixel_cache.h: 39

ConstantVirtualPixelMethod = (UndefinedVirtualPixelMethod + 1) # /tmp/tmpu80Elu/pixel_cache.h: 39

EdgeVirtualPixelMethod = (ConstantVirtualPixelMethod + 1) # /tmp/tmpu80Elu/pixel_cache.h: 39

MirrorVirtualPixelMethod = (EdgeVirtualPixelMethod + 1) # /tmp/tmpu80Elu/pixel_cache.h: 39

TileVirtualPixelMethod = (MirrorVirtualPixelMethod + 1) # /tmp/tmpu80Elu/pixel_cache.h: 39

VirtualPixelMethod = enum_anon_34 # /tmp/tmpu80Elu/pixel_cache.h: 39

Cache = _CacheInfoPtr_ # /tmp/tmpu80Elu/pixel_cache.h: 44

# /tmp/tmpu80Elu/pixel_cache.h: 56
if hasattr(_libs['GraphicsMagick'], 'AcquireImagePixels'):
    AcquireImagePixels = _libs['GraphicsMagick'].AcquireImagePixels
    AcquireImagePixels.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    AcquireImagePixels.restype = POINTER(PixelPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 66
if hasattr(_libs['GraphicsMagick'], 'AccessImmutableIndexes'):
    AccessImmutableIndexes = _libs['GraphicsMagick'].AccessImmutableIndexes
    AccessImmutableIndexes.argtypes = [POINTER(Image)]
    AccessImmutableIndexes.restype = POINTER(IndexPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 74
if hasattr(_libs['GraphicsMagick'], 'AcquireOnePixel'):
    AcquireOnePixel = _libs['GraphicsMagick'].AcquireOnePixel
    AcquireOnePixel.argtypes = [POINTER(Image), c_long, c_long, POINTER(ExceptionInfo)]
    AcquireOnePixel.restype = PixelPacket

# /tmp/tmpu80Elu/pixel_cache.h: 83
if hasattr(_libs['GraphicsMagick'], 'GetImagePixels'):
    GetImagePixels = _libs['GraphicsMagick'].GetImagePixels
    GetImagePixels.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong]
    GetImagePixels.restype = POINTER(PixelPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 86
if hasattr(_libs['GraphicsMagick'], 'GetImagePixelsEx'):
    GetImagePixelsEx = _libs['GraphicsMagick'].GetImagePixelsEx
    GetImagePixelsEx.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    GetImagePixelsEx.restype = POINTER(PixelPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 95
if hasattr(_libs['GraphicsMagick'], 'GetImageVirtualPixelMethod'):
    GetImageVirtualPixelMethod = _libs['GraphicsMagick'].GetImageVirtualPixelMethod
    GetImageVirtualPixelMethod.argtypes = [POINTER(Image)]
    GetImageVirtualPixelMethod.restype = VirtualPixelMethod

# /tmp/tmpu80Elu/pixel_cache.h: 102
if hasattr(_libs['GraphicsMagick'], 'GetPixels'):
    GetPixels = _libs['GraphicsMagick'].GetPixels
    GetPixels.argtypes = [POINTER(Image)]
    GetPixels.restype = POINTER(PixelPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 104
if hasattr(_libs['GraphicsMagick'], 'AccessMutablePixels'):
    AccessMutablePixels = _libs['GraphicsMagick'].AccessMutablePixels
    AccessMutablePixels.argtypes = [POINTER(Image)]
    AccessMutablePixels.restype = POINTER(PixelPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 112
if hasattr(_libs['GraphicsMagick'], 'GetIndexes'):
    GetIndexes = _libs['GraphicsMagick'].GetIndexes
    GetIndexes.argtypes = [POINTER(Image)]
    GetIndexes.restype = POINTER(IndexPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 114
if hasattr(_libs['GraphicsMagick'], 'AccessMutableIndexes'):
    AccessMutableIndexes = _libs['GraphicsMagick'].AccessMutableIndexes
    AccessMutableIndexes.argtypes = [POINTER(Image)]
    AccessMutableIndexes.restype = POINTER(IndexPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 124
if hasattr(_libs['GraphicsMagick'], 'GetOnePixel'):
    GetOnePixel = _libs['GraphicsMagick'].GetOnePixel
    GetOnePixel.argtypes = [POINTER(Image), c_long, c_long]
    GetOnePixel.restype = PixelPacket

# /tmp/tmpu80Elu/pixel_cache.h: 131
if hasattr(_libs['GraphicsMagick'], 'GetPixelCacheArea'):
    GetPixelCacheArea = _libs['GraphicsMagick'].GetPixelCacheArea
    GetPixelCacheArea.argtypes = [POINTER(Image)]
    GetPixelCacheArea.restype = magick_off_t

# /tmp/tmpu80Elu/pixel_cache.h: 138
if hasattr(_libs['GraphicsMagick'], 'SetImagePixels'):
    SetImagePixels = _libs['GraphicsMagick'].SetImagePixels
    SetImagePixels.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong]
    SetImagePixels.restype = POINTER(PixelPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 141
if hasattr(_libs['GraphicsMagick'], 'SetImagePixelsEx'):
    SetImagePixelsEx = _libs['GraphicsMagick'].SetImagePixelsEx
    SetImagePixelsEx.argtypes = [POINTER(Image), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    SetImagePixelsEx.restype = POINTER(PixelPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 150
if hasattr(_libs['GraphicsMagick'], 'SetImageVirtualPixelMethod'):
    SetImageVirtualPixelMethod = _libs['GraphicsMagick'].SetImageVirtualPixelMethod
    SetImageVirtualPixelMethod.argtypes = [POINTER(Image), VirtualPixelMethod]
    SetImageVirtualPixelMethod.restype = c_uint

# /tmp/tmpu80Elu/pixel_cache.h: 158
if hasattr(_libs['GraphicsMagick'], 'SyncImagePixels'):
    SyncImagePixels = _libs['GraphicsMagick'].SyncImagePixels
    SyncImagePixels.argtypes = [POINTER(Image)]
    SyncImagePixels.restype = c_uint

# /tmp/tmpu80Elu/pixel_cache.h: 160
if hasattr(_libs['GraphicsMagick'], 'SyncImagePixelsEx'):
    SyncImagePixelsEx = _libs['GraphicsMagick'].SyncImagePixelsEx
    SyncImagePixelsEx.argtypes = [POINTER(Image), POINTER(ExceptionInfo)]
    SyncImagePixelsEx.restype = c_uint

# /tmp/tmpu80Elu/pixel_cache.h: 172
if hasattr(_libs['GraphicsMagick'], 'OpenCacheView'):
    OpenCacheView = _libs['GraphicsMagick'].OpenCacheView
    OpenCacheView.argtypes = [POINTER(Image)]
    OpenCacheView.restype = POINTER(ViewInfo)

# /tmp/tmpu80Elu/pixel_cache.h: 178
if hasattr(_libs['GraphicsMagick'], 'CloseCacheView'):
    CloseCacheView = _libs['GraphicsMagick'].CloseCacheView
    CloseCacheView.argtypes = [POINTER(ViewInfo)]
    CloseCacheView.restype = None

# /tmp/tmpu80Elu/pixel_cache.h: 187
if hasattr(_libs['GraphicsMagick'], 'AccessCacheViewPixels'):
    AccessCacheViewPixels = _libs['GraphicsMagick'].AccessCacheViewPixels
    AccessCacheViewPixels.argtypes = [POINTER(ViewInfo)]
    AccessCacheViewPixels.restype = POINTER(PixelPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 194
if hasattr(_libs['GraphicsMagick'], 'AcquireCacheViewIndexes'):
    AcquireCacheViewIndexes = _libs['GraphicsMagick'].AcquireCacheViewIndexes
    AcquireCacheViewIndexes.argtypes = [POINTER(ViewInfo)]
    AcquireCacheViewIndexes.restype = POINTER(IndexPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 201
if hasattr(_libs['GraphicsMagick'], 'AcquireCacheViewPixels'):
    AcquireCacheViewPixels = _libs['GraphicsMagick'].AcquireCacheViewPixels
    AcquireCacheViewPixels.argtypes = [POINTER(ViewInfo), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    AcquireCacheViewPixels.restype = POINTER(PixelPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 213
if hasattr(_libs['GraphicsMagick'], 'AcquireOneCacheViewPixel'):
    AcquireOneCacheViewPixel = _libs['GraphicsMagick'].AcquireOneCacheViewPixel
    AcquireOneCacheViewPixel.argtypes = [POINTER(ViewInfo), POINTER(PixelPacket), c_long, c_long, POINTER(ExceptionInfo)]
    AcquireOneCacheViewPixel.restype = c_uint

# /tmp/tmpu80Elu/pixel_cache.h: 221
if hasattr(_libs['GraphicsMagick'], 'GetCacheViewArea'):
    GetCacheViewArea = _libs['GraphicsMagick'].GetCacheViewArea
    GetCacheViewArea.argtypes = [POINTER(ViewInfo)]
    GetCacheViewArea.restype = magick_off_t

# /tmp/tmpu80Elu/pixel_cache.h: 226
if hasattr(_libs['GraphicsMagick'], 'GetCacheViewImage'):
    GetCacheViewImage = _libs['GraphicsMagick'].GetCacheViewImage
    GetCacheViewImage.argtypes = [POINTER(ViewInfo)]
    GetCacheViewImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/pixel_cache.h: 233
if hasattr(_libs['GraphicsMagick'], 'GetCacheViewIndexes'):
    GetCacheViewIndexes = _libs['GraphicsMagick'].GetCacheViewIndexes
    GetCacheViewIndexes.argtypes = [POINTER(ViewInfo)]
    GetCacheViewIndexes.restype = POINTER(IndexPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 240
if hasattr(_libs['GraphicsMagick'], 'GetCacheViewPixels'):
    GetCacheViewPixels = _libs['GraphicsMagick'].GetCacheViewPixels
    GetCacheViewPixels.argtypes = [POINTER(ViewInfo), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    GetCacheViewPixels.restype = POINTER(PixelPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 248
if hasattr(_libs['GraphicsMagick'], 'GetCacheViewRegion'):
    GetCacheViewRegion = _libs['GraphicsMagick'].GetCacheViewRegion
    GetCacheViewRegion.argtypes = [POINTER(ViewInfo)]
    GetCacheViewRegion.restype = RectangleInfo

# /tmp/tmpu80Elu/pixel_cache.h: 256
if hasattr(_libs['GraphicsMagick'], 'SetCacheViewPixels'):
    SetCacheViewPixels = _libs['GraphicsMagick'].SetCacheViewPixels
    SetCacheViewPixels.argtypes = [POINTER(ViewInfo), c_long, c_long, c_ulong, c_ulong, POINTER(ExceptionInfo)]
    SetCacheViewPixels.restype = POINTER(PixelPacket)

# /tmp/tmpu80Elu/pixel_cache.h: 264
if hasattr(_libs['GraphicsMagick'], 'SyncCacheViewPixels'):
    SyncCacheViewPixels = _libs['GraphicsMagick'].SyncCacheViewPixels
    SyncCacheViewPixels.argtypes = [POINTER(ViewInfo), POINTER(ExceptionInfo)]
    SyncCacheViewPixels.restype = c_uint

BlobInfo = struct__BlobInfo # /tmp/tmpu80Elu/blob.h: 37

# /tmp/tmpu80Elu/blob.h: 49
if hasattr(_libs['GraphicsMagick'], 'CloneBlobInfo'):
    CloneBlobInfo = _libs['GraphicsMagick'].CloneBlobInfo
    CloneBlobInfo.argtypes = [POINTER(BlobInfo)]
    CloneBlobInfo.restype = POINTER(BlobInfo)

# /tmp/tmpu80Elu/blob.h: 55
if hasattr(_libs['GraphicsMagick'], 'ReferenceBlob'):
    ReferenceBlob = _libs['GraphicsMagick'].ReferenceBlob
    ReferenceBlob.argtypes = [POINTER(BlobInfo)]
    ReferenceBlob.restype = POINTER(BlobInfo)

# /tmp/tmpu80Elu/blob.h: 60
if hasattr(_libs['GraphicsMagick'], 'DestroyBlobInfo'):
    DestroyBlobInfo = _libs['GraphicsMagick'].DestroyBlobInfo
    DestroyBlobInfo.argtypes = [POINTER(BlobInfo)]
    DestroyBlobInfo.restype = None

# /tmp/tmpu80Elu/blob.h: 66
if hasattr(_libs['GraphicsMagick'], 'DetachBlob'):
    DetachBlob = _libs['GraphicsMagick'].DetachBlob
    DetachBlob.argtypes = [POINTER(BlobInfo)]
    DetachBlob.restype = None

# /tmp/tmpu80Elu/blob.h: 71
if hasattr(_libs['GraphicsMagick'], 'GetBlobInfo'):
    GetBlobInfo = _libs['GraphicsMagick'].GetBlobInfo
    GetBlobInfo.argtypes = [POINTER(BlobInfo)]
    GetBlobInfo.restype = None

# /tmp/tmpu80Elu/blob.h: 76
if hasattr(_libs['GraphicsMagick'], 'AttachBlob'):
    AttachBlob = _libs['GraphicsMagick'].AttachBlob
    AttachBlob.argtypes = [POINTER(BlobInfo), POINTER(None), c_size_t]
    AttachBlob.restype = None

# /tmp/tmpu80Elu/blob.h: 89
if hasattr(_libs['GraphicsMagick'], 'DestroyBlob'):
    DestroyBlob = _libs['GraphicsMagick'].DestroyBlob
    DestroyBlob.argtypes = [POINTER(Image)]
    DestroyBlob.restype = None

# /tmp/tmpu80Elu/blob.h: 101
if hasattr(_libs['GraphicsMagick'], 'BlobToImage'):
    BlobToImage = _libs['GraphicsMagick'].BlobToImage
    BlobToImage.argtypes = [POINTER(ImageInfo), POINTER(None), c_size_t, POINTER(ExceptionInfo)]
    BlobToImage.restype = POINTER(Image)

# /tmp/tmpu80Elu/blob.h: 111
if hasattr(_libs['GraphicsMagick'], 'PingBlob'):
    PingBlob = _libs['GraphicsMagick'].PingBlob
    PingBlob.argtypes = [POINTER(ImageInfo), POINTER(None), c_size_t, POINTER(ExceptionInfo)]
    PingBlob.restype = POINTER(Image)

# /tmp/tmpu80Elu/blob.h: 120
if hasattr(_libs['GraphicsMagick'], 'ImageToBlob'):
    ImageToBlob = _libs['GraphicsMagick'].ImageToBlob
    ImageToBlob.argtypes = [POINTER(ImageInfo), POINTER(Image), POINTER(c_size_t), POINTER(ExceptionInfo)]
    ImageToBlob.restype = POINTER(None)

enum_anon_35 = c_int # /tmp/tmpu80Elu/blob.h: 141

UndefinedBlobMode = 0 # /tmp/tmpu80Elu/blob.h: 141

ReadBlobMode = (UndefinedBlobMode + 1) # /tmp/tmpu80Elu/blob.h: 141

ReadBinaryBlobMode = (ReadBlobMode + 1) # /tmp/tmpu80Elu/blob.h: 141

WriteBlobMode = (ReadBinaryBlobMode + 1) # /tmp/tmpu80Elu/blob.h: 141

WriteBinaryBlobMode = (WriteBlobMode + 1) # /tmp/tmpu80Elu/blob.h: 141

BlobMode = enum_anon_35 # /tmp/tmpu80Elu/blob.h: 141

# /tmp/tmpu80Elu/blob.h: 147
if hasattr(_libs['GraphicsMagick'], 'OpenBlob'):
    OpenBlob = _libs['GraphicsMagick'].OpenBlob
    OpenBlob.argtypes = [POINTER(ImageInfo), POINTER(Image), BlobMode, POINTER(ExceptionInfo)]
    OpenBlob.restype = c_uint

# /tmp/tmpu80Elu/blob.h: 155
if hasattr(_libs['GraphicsMagick'], 'CloseBlob'):
    CloseBlob = _libs['GraphicsMagick'].CloseBlob
    CloseBlob.argtypes = [POINTER(Image)]
    CloseBlob.restype = None

# /tmp/tmpu80Elu/blob.h: 161
if hasattr(_libs['GraphicsMagick'], 'ReadBlob'):
    ReadBlob = _libs['GraphicsMagick'].ReadBlob
    ReadBlob.argtypes = [POINTER(Image), c_size_t, POINTER(None)]
    ReadBlob.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 169
if hasattr(_libs['GraphicsMagick'], 'ReadBlobZC'):
    ReadBlobZC = _libs['GraphicsMagick'].ReadBlobZC
    ReadBlobZC.argtypes = [POINTER(Image), c_size_t, POINTER(POINTER(None))]
    ReadBlobZC.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 176
if hasattr(_libs['GraphicsMagick'], 'WriteBlob'):
    WriteBlob = _libs['GraphicsMagick'].WriteBlob
    WriteBlob.argtypes = [POINTER(Image), c_size_t, POINTER(None)]
    WriteBlob.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 183
if hasattr(_libs['GraphicsMagick'], 'SeekBlob'):
    SeekBlob = _libs['GraphicsMagick'].SeekBlob
    SeekBlob.argtypes = [POINTER(Image), magick_off_t, c_int]
    SeekBlob.restype = magick_off_t

# /tmp/tmpu80Elu/blob.h: 191
if hasattr(_libs['GraphicsMagick'], 'TellBlob'):
    TellBlob = _libs['GraphicsMagick'].TellBlob
    TellBlob.argtypes = [POINTER(Image)]
    TellBlob.restype = magick_off_t

# /tmp/tmpu80Elu/blob.h: 196
if hasattr(_libs['GraphicsMagick'], 'EOFBlob'):
    EOFBlob = _libs['GraphicsMagick'].EOFBlob
    EOFBlob.argtypes = [POINTER(Image)]
    EOFBlob.restype = c_int

# /tmp/tmpu80Elu/blob.h: 202
if hasattr(_libs['GraphicsMagick'], 'GetBlobStatus'):
    GetBlobStatus = _libs['GraphicsMagick'].GetBlobStatus
    GetBlobStatus.argtypes = [POINTER(Image)]
    GetBlobStatus.restype = c_int

# /tmp/tmpu80Elu/blob.h: 208
if hasattr(_libs['GraphicsMagick'], 'GetBlobSize'):
    GetBlobSize = _libs['GraphicsMagick'].GetBlobSize
    GetBlobSize.argtypes = [POINTER(Image)]
    GetBlobSize.restype = magick_off_t

# /tmp/tmpu80Elu/blob.h: 214
if hasattr(_libs['GraphicsMagick'], 'GetBlobFileHandle'):
    GetBlobFileHandle = _libs['GraphicsMagick'].GetBlobFileHandle
    GetBlobFileHandle.argtypes = [POINTER(Image)]
    GetBlobFileHandle.restype = POINTER(FILE)

# /tmp/tmpu80Elu/blob.h: 221
if hasattr(_libs['GraphicsMagick'], 'GetBlobStreamData'):
    GetBlobStreamData = _libs['GraphicsMagick'].GetBlobStreamData
    GetBlobStreamData.argtypes = [POINTER(Image)]
    GetBlobStreamData.restype = POINTER(c_ubyte)

# /tmp/tmpu80Elu/blob.h: 234
if hasattr(_libs['GraphicsMagick'], 'ReadBlobByte'):
    ReadBlobByte = _libs['GraphicsMagick'].ReadBlobByte
    ReadBlobByte.argtypes = [POINTER(Image)]
    ReadBlobByte.restype = c_int

# /tmp/tmpu80Elu/blob.h: 240
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBShort'):
    ReadBlobLSBShort = _libs['GraphicsMagick'].ReadBlobLSBShort
    ReadBlobLSBShort.argtypes = [POINTER(Image)]
    ReadBlobLSBShort.restype = magick_uint16_t

# /tmp/tmpu80Elu/blob.h: 246
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBShorts'):
    ReadBlobLSBShorts = _libs['GraphicsMagick'].ReadBlobLSBShorts
    ReadBlobLSBShorts.argtypes = [POINTER(Image), c_size_t, POINTER(magick_uint16_t)]
    ReadBlobLSBShorts.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 253
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBShort'):
    ReadBlobMSBShort = _libs['GraphicsMagick'].ReadBlobMSBShort
    ReadBlobMSBShort.argtypes = [POINTER(Image)]
    ReadBlobMSBShort.restype = magick_uint16_t

# /tmp/tmpu80Elu/blob.h: 259
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBShorts'):
    ReadBlobMSBShorts = _libs['GraphicsMagick'].ReadBlobMSBShorts
    ReadBlobMSBShorts.argtypes = [POINTER(Image), c_size_t, POINTER(magick_uint16_t)]
    ReadBlobMSBShorts.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 265
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBLong'):
    ReadBlobLSBLong = _libs['GraphicsMagick'].ReadBlobLSBLong
    ReadBlobLSBLong.argtypes = [POINTER(Image)]
    ReadBlobLSBLong.restype = magick_uint32_t

# /tmp/tmpu80Elu/blob.h: 271
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBLongs'):
    ReadBlobLSBLongs = _libs['GraphicsMagick'].ReadBlobLSBLongs
    ReadBlobLSBLongs.argtypes = [POINTER(Image), c_size_t, POINTER(magick_uint32_t)]
    ReadBlobLSBLongs.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 277
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBLong'):
    ReadBlobMSBLong = _libs['GraphicsMagick'].ReadBlobMSBLong
    ReadBlobMSBLong.argtypes = [POINTER(Image)]
    ReadBlobMSBLong.restype = magick_uint32_t

# /tmp/tmpu80Elu/blob.h: 282
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBLongs'):
    ReadBlobMSBLongs = _libs['GraphicsMagick'].ReadBlobMSBLongs
    ReadBlobMSBLongs.argtypes = [POINTER(Image), c_size_t, POINTER(magick_uint32_t)]
    ReadBlobMSBLongs.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 288
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBFloat'):
    ReadBlobLSBFloat = _libs['GraphicsMagick'].ReadBlobLSBFloat
    ReadBlobLSBFloat.argtypes = [POINTER(Image)]
    ReadBlobLSBFloat.restype = c_float

# /tmp/tmpu80Elu/blob.h: 294
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBFloats'):
    ReadBlobLSBFloats = _libs['GraphicsMagick'].ReadBlobLSBFloats
    ReadBlobLSBFloats.argtypes = [POINTER(Image), c_size_t, POINTER(c_float)]
    ReadBlobLSBFloats.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 300
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBFloat'):
    ReadBlobMSBFloat = _libs['GraphicsMagick'].ReadBlobMSBFloat
    ReadBlobMSBFloat.argtypes = [POINTER(Image)]
    ReadBlobMSBFloat.restype = c_float

# /tmp/tmpu80Elu/blob.h: 306
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBFloats'):
    ReadBlobMSBFloats = _libs['GraphicsMagick'].ReadBlobMSBFloats
    ReadBlobMSBFloats.argtypes = [POINTER(Image), c_size_t, POINTER(c_float)]
    ReadBlobMSBFloats.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 312
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBDouble'):
    ReadBlobLSBDouble = _libs['GraphicsMagick'].ReadBlobLSBDouble
    ReadBlobLSBDouble.argtypes = [POINTER(Image)]
    ReadBlobLSBDouble.restype = c_double

# /tmp/tmpu80Elu/blob.h: 318
if hasattr(_libs['GraphicsMagick'], 'ReadBlobLSBDoubles'):
    ReadBlobLSBDoubles = _libs['GraphicsMagick'].ReadBlobLSBDoubles
    ReadBlobLSBDoubles.argtypes = [POINTER(Image), c_size_t, POINTER(c_double)]
    ReadBlobLSBDoubles.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 324
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBDouble'):
    ReadBlobMSBDouble = _libs['GraphicsMagick'].ReadBlobMSBDouble
    ReadBlobMSBDouble.argtypes = [POINTER(Image)]
    ReadBlobMSBDouble.restype = c_double

# /tmp/tmpu80Elu/blob.h: 329
if hasattr(_libs['GraphicsMagick'], 'ReadBlobMSBDoubles'):
    ReadBlobMSBDoubles = _libs['GraphicsMagick'].ReadBlobMSBDoubles
    ReadBlobMSBDoubles.argtypes = [POINTER(Image), c_size_t, POINTER(c_double)]
    ReadBlobMSBDoubles.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 336
if hasattr(_libs['GraphicsMagick'], 'ReadBlobString'):
    ReadBlobString = _libs['GraphicsMagick'].ReadBlobString
    ReadBlobString.argtypes = [POINTER(Image), String]
    if sizeof(c_int) == sizeof(c_void_p):
        ReadBlobString.restype = ReturnString
    else:
        ReadBlobString.restype = String
        ReadBlobString.errcheck = ReturnString

# /tmp/tmpu80Elu/blob.h: 342
if hasattr(_libs['GraphicsMagick'], 'WriteBlobByte'):
    WriteBlobByte = _libs['GraphicsMagick'].WriteBlobByte
    WriteBlobByte.argtypes = [POINTER(Image), magick_uint8_t]
    WriteBlobByte.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 348
if hasattr(_libs['GraphicsMagick'], 'WriteBlobFile'):
    WriteBlobFile = _libs['GraphicsMagick'].WriteBlobFile
    WriteBlobFile.argtypes = [POINTER(Image), String]
    WriteBlobFile.restype = c_uint

# /tmp/tmpu80Elu/blob.h: 354
if hasattr(_libs['GraphicsMagick'], 'WriteBlobLSBShort'):
    WriteBlobLSBShort = _libs['GraphicsMagick'].WriteBlobLSBShort
    WriteBlobLSBShort.argtypes = [POINTER(Image), magick_uint16_t]
    WriteBlobLSBShort.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 360
if hasattr(_libs['GraphicsMagick'], 'WriteBlobLSBLong'):
    WriteBlobLSBLong = _libs['GraphicsMagick'].WriteBlobLSBLong
    WriteBlobLSBLong.argtypes = [POINTER(Image), magick_uint32_t]
    WriteBlobLSBLong.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 368
if hasattr(_libs['GraphicsMagick'], 'WriteBlobMSBLong'):
    WriteBlobMSBLong = _libs['GraphicsMagick'].WriteBlobMSBLong
    WriteBlobMSBLong.argtypes = [POINTER(Image), magick_uint32_t]
    WriteBlobMSBLong.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 374
if hasattr(_libs['GraphicsMagick'], 'WriteBlobMSBShort'):
    WriteBlobMSBShort = _libs['GraphicsMagick'].WriteBlobMSBShort
    WriteBlobMSBShort.argtypes = [POINTER(Image), magick_uint16_t]
    WriteBlobMSBShort.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 381
if hasattr(_libs['GraphicsMagick'], 'WriteBlobString'):
    WriteBlobString = _libs['GraphicsMagick'].WriteBlobString
    WriteBlobString.argtypes = [POINTER(Image), String]
    WriteBlobString.restype = c_size_t

# /tmp/tmpu80Elu/blob.h: 394
if hasattr(_libs['GraphicsMagick'], 'BlobIsSeekable'):
    BlobIsSeekable = _libs['GraphicsMagick'].BlobIsSeekable
    BlobIsSeekable.argtypes = [POINTER(Image)]
    BlobIsSeekable.restype = c_uint

# /tmp/tmpu80Elu/blob.h: 399
if hasattr(_libs['GraphicsMagick'], 'SetBlobClosable'):
    SetBlobClosable = _libs['GraphicsMagick'].SetBlobClosable
    SetBlobClosable.argtypes = [POINTER(Image), c_uint]
    SetBlobClosable.restype = None

# /tmp/tmpu80Elu/blob.h: 405
if hasattr(_libs['GraphicsMagick'], 'SetBlobTemporary'):
    SetBlobTemporary = _libs['GraphicsMagick'].SetBlobTemporary
    SetBlobTemporary.argtypes = [POINTER(Image), c_uint]
    SetBlobTemporary.restype = None

# /tmp/tmpu80Elu/blob.h: 412
if hasattr(_libs['GraphicsMagick'], 'GetBlobTemporary'):
    GetBlobTemporary = _libs['GraphicsMagick'].GetBlobTemporary
    GetBlobTemporary.argtypes = [POINTER(Image)]
    GetBlobTemporary.restype = c_uint

enum_anon_36 = c_int # /tmp/tmpu80Elu/blob.h: 428

ReadMode = 0 # /tmp/tmpu80Elu/blob.h: 428

WriteMode = (ReadMode + 1) # /tmp/tmpu80Elu/blob.h: 428

IOMode = (WriteMode + 1) # /tmp/tmpu80Elu/blob.h: 428

MapMode = enum_anon_36 # /tmp/tmpu80Elu/blob.h: 428

# /tmp/tmpu80Elu/blob.h: 433
if hasattr(_libs['GraphicsMagick'], 'UnmapBlob'):
    UnmapBlob = _libs['GraphicsMagick'].UnmapBlob
    UnmapBlob.argtypes = [POINTER(None), c_size_t]
    UnmapBlob.restype = c_uint

# /tmp/tmpu80Elu/blob.h: 439
if hasattr(_libs['GraphicsMagick'], 'MapBlob'):
    MapBlob = _libs['GraphicsMagick'].MapBlob
    MapBlob.argtypes = [c_int, MapMode, magick_off_t, c_size_t]
    MapBlob.restype = POINTER(None)

# /tmp/tmpu80Elu/blob.h: 453
if hasattr(_libs['GraphicsMagick'], 'BlobToFile'):
    BlobToFile = _libs['GraphicsMagick'].BlobToFile
    BlobToFile.argtypes = [String, POINTER(None), c_size_t, POINTER(ExceptionInfo)]
    BlobToFile.restype = c_uint

# /tmp/tmpu80Elu/blob.h: 461
if hasattr(_libs['GraphicsMagick'], 'FileToBlob'):
    FileToBlob = _libs['GraphicsMagick'].FileToBlob
    FileToBlob.argtypes = [String, POINTER(c_size_t), POINTER(ExceptionInfo)]
    FileToBlob.restype = POINTER(None)

# /tmp/tmpu80Elu/blob.h: 474
if hasattr(_libs['GraphicsMagick'], 'BlobReserveSize'):
    BlobReserveSize = _libs['GraphicsMagick'].BlobReserveSize
    BlobReserveSize.argtypes = [POINTER(Image), magick_off_t]
    BlobReserveSize.restype = c_uint

# /tmp/tmpu80Elu/blob.h: 480
if hasattr(_libs['GraphicsMagick'], 'ImageToFile'):
    ImageToFile = _libs['GraphicsMagick'].ImageToFile
    ImageToFile.argtypes = [POINTER(Image), String, POINTER(ExceptionInfo)]
    ImageToFile.restype = c_uint

# /tmp/tmpu80Elu/blob.h: 488
if hasattr(_libs['GraphicsMagick'], 'GetConfigureBlob'):
    GetConfigureBlob = _libs['GraphicsMagick'].GetConfigureBlob
    GetConfigureBlob.argtypes = [String, String, POINTER(c_size_t), POINTER(ExceptionInfo)]
    GetConfigureBlob.restype = POINTER(None)

# /tmp/tmpu80Elu/blob.h: 497
if hasattr(_libs['GraphicsMagick'], 'MSBOrderLong'):
    MSBOrderLong = _libs['GraphicsMagick'].MSBOrderLong
    MSBOrderLong.argtypes = [POINTER(c_ubyte), c_size_t]
    MSBOrderLong.restype = None

# /tmp/tmpu80Elu/blob.h: 504
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

ImageAttribute = struct__ImageAttribute # /tmp/tmpu80Elu/attribute.h: 40

# /tmp/tmpu80Elu/attribute.h: 46
if hasattr(_libs['GraphicsMagick'], 'GetImageAttribute'):
    GetImageAttribute = _libs['GraphicsMagick'].GetImageAttribute
    GetImageAttribute.argtypes = [POINTER(Image), String]
    GetImageAttribute.restype = POINTER(ImageAttribute)

# /tmp/tmpu80Elu/attribute.h: 46
if hasattr(_libs['GraphicsMagick'], 'GetImageClippingPathAttribute'):
    GetImageClippingPathAttribute = _libs['GraphicsMagick'].GetImageClippingPathAttribute
    GetImageClippingPathAttribute.argtypes = [POINTER(Image)]
    GetImageClippingPathAttribute.restype = POINTER(ImageAttribute)

# /tmp/tmpu80Elu/attribute.h: 46
if hasattr(_libs['GraphicsMagick'], 'GetImageInfoAttribute'):
    GetImageInfoAttribute = _libs['GraphicsMagick'].GetImageInfoAttribute
    GetImageInfoAttribute.argtypes = [POINTER(ImageInfo), POINTER(Image), String]
    GetImageInfoAttribute.restype = POINTER(ImageAttribute)

# /tmp/tmpu80Elu/attribute.h: 51
if hasattr(_libs['GraphicsMagick'], 'CloneImageAttributes'):
    CloneImageAttributes = _libs['GraphicsMagick'].CloneImageAttributes
    CloneImageAttributes.argtypes = [POINTER(Image), POINTER(Image)]
    CloneImageAttributes.restype = c_uint

# /tmp/tmpu80Elu/attribute.h: 51
if hasattr(_libs['GraphicsMagick'], 'SetImageAttribute'):
    SetImageAttribute = _libs['GraphicsMagick'].SetImageAttribute
    SetImageAttribute.argtypes = [POINTER(Image), String, String]
    SetImageAttribute.restype = c_uint

# /tmp/tmpu80Elu/attribute.h: 55
if hasattr(_libs['GraphicsMagick'], 'DestroyImageAttributes'):
    DestroyImageAttributes = _libs['GraphicsMagick'].DestroyImageAttributes
    DestroyImageAttributes.argtypes = [POINTER(Image)]
    DestroyImageAttributes.restype = None

# gm_headers/magick/magick_config.h: 22
try:
    MaxRGB = 255
except:
    pass

# gm_headers/magick/magick_config.h: 23
try:
    MaxRGBFloat = 255.0
except:
    pass

# gm_headers/magick/magick_config.h: 24
try:
    MaxRGBDouble = 255.0
except:
    pass

# gm_headers/magick/common.h: 101
try:
    MagickFalse = 0
except:
    pass

# /tmp/tmpu80Elu/image.h: 45
def MaxValueGivenBits(bits):
    return ((1L << (bits - 1)) + ((1L << (bits - 1)) - 1))

# /tmp/tmpu80Elu/image.h: 48
try:
    MaxColormapSize = 256
except:
    pass

# /tmp/tmpu80Elu/image.h: 49
try:
    MaxMap = 255
except:
    pass

# /tmp/tmpu80Elu/image.h: 50
try:
    MaxMapFloat = 255.0
except:
    pass

# /tmp/tmpu80Elu/image.h: 51
try:
    MaxMapDouble = 255.0
except:
    pass

# /tmp/tmpu80Elu/image.h: 52
try:
    MaxRGB = 255
except:
    pass

# /tmp/tmpu80Elu/image.h: 53
try:
    MaxRGBFloat = 255.0
except:
    pass

# /tmp/tmpu80Elu/image.h: 54
try:
    MaxRGBDouble = 255.0
except:
    pass

# /tmp/tmpu80Elu/image.h: 55
def ScaleCharToMap(value):
    return value

# /tmp/tmpu80Elu/image.h: 56
def ScaleCharToQuantum(value):
    return value

# /tmp/tmpu80Elu/image.h: 57
def ScaleLongToQuantum(value):
    return (value / 16843009L)

# /tmp/tmpu80Elu/image.h: 58
def ScaleMapToChar(value):
    return value

# /tmp/tmpu80Elu/image.h: 59
def ScaleMapToQuantum(value):
    return value

# /tmp/tmpu80Elu/image.h: 60
def ScaleQuantum(quantum):
    return quantum

# /tmp/tmpu80Elu/image.h: 61
def ScaleQuantumToChar(quantum):
    return quantum

# /tmp/tmpu80Elu/image.h: 62
def ScaleQuantumToLong(quantum):
    return (16843009L * quantum)

# /tmp/tmpu80Elu/image.h: 63
def ScaleQuantumToMap(quantum):
    return quantum

# /tmp/tmpu80Elu/image.h: 64
def ScaleQuantumToShort(quantum):
    return (257 * quantum)

# /tmp/tmpu80Elu/image.h: 65
def ScaleShortToQuantum(value):
    return (value / 257)

# /tmp/tmpu80Elu/image.h: 66
def ScaleToQuantum(value):
    return value

# /tmp/tmpu80Elu/image.h: 67
def ScaleQuantumToIndex(value):
    return value

# /tmp/tmpu80Elu/image.h: 137
try:
    OpaqueOpacity = 0L
except:
    pass

# /tmp/tmpu80Elu/image.h: 138
try:
    TransparentOpacity = MaxRGB
except:
    pass

# /tmp/tmpu80Elu/image.h: 139
def RoundDoubleToQuantum(value):
    return (value < 0.0) and 0 or (value > MaxRGBDouble) and MaxRGB or (value + 0.5)

# /tmp/tmpu80Elu/image.h: 141
def RoundFloatToQuantum(value):
    return (value < 0.0) and 0 or (value > MaxRGBFloat) and MaxRGB or (value + 0.5)

# /tmp/tmpu80Elu/image.h: 143
def ConstrainToRange(min, max, value):
    return (value < min) and min or (value > max) and max or value

# /tmp/tmpu80Elu/image.h: 145
def ConstrainToQuantum(value):
    return (ConstrainToRange (0, MaxRGB, value))

# /tmp/tmpu80Elu/image.h: 146
def ScaleAnyToQuantum(x, max_value):
    return (((MaxRGBDouble * x) / max_value) + 0.5)

# /tmp/tmpu80Elu/image.h: 148
def MagickBoolToString(value):
    return (value != MagickFalse) and 'True' or 'False'

# /tmp/tmpu80Elu/image.h: 154
def MagickChannelEnabled(channels, channel):
    return ((channels == AllChannels) or (channels == channel))

# /tmp/tmpu80Elu/image.h: 159
try:
    RunlengthEncodedCompression = RLECompression
except:
    pass

# /tmp/tmpu80Elu/image.h: 160
def RoundSignedToQuantum(value):
    return (RoundDoubleToQuantum (value))

# /tmp/tmpu80Elu/image.h: 161
def RoundToQuantum(value):
    return (RoundDoubleToQuantum (value))

# /tmp/tmpu80Elu/image.h: 527
try:
    MAGICK_PIXELS_BGRA = 1
except:
    pass

# /tmp/tmpu80Elu/resize.h: 26
try:
    DefaultResizeFilter = LanczosFilter
except:
    pass

# /tmp/tmpu80Elu/blob.h: 32
try:
    MinBlobExtent = 32768L
except:
    pass

_Image = struct__Image # /tmp/tmpu80Elu/image.h: 649

_ImageAttribute = struct__ImageAttribute # /tmp/tmpu80Elu/attribute.h: 28

_ExceptionInfo = struct__ExceptionInfo # gm_headers/magick/error.h: 226

_AffineMatrix = struct__AffineMatrix # /tmp/tmpu80Elu/image.h: 459

_PrimaryInfo = struct__PrimaryInfo # /tmp/tmpu80Elu/image.h: 467

_ChromaticityInfo = struct__ChromaticityInfo # /tmp/tmpu80Elu/image.h: 476

_PixelPacket = struct__PixelPacket # /tmp/tmpu80Elu/image.h: 534

_DoublePixelPacket = struct__DoublePixelPacket # /tmp/tmpu80Elu/image.h: 543

_ErrorInfo = struct__ErrorInfo # /tmp/tmpu80Elu/image.h: 555

_FrameInfo = struct__FrameInfo # /tmp/tmpu80Elu/image.h: 568

_LongPixelPacket = struct__LongPixelPacket # /tmp/tmpu80Elu/image.h: 579

_MontageInfo = struct__MontageInfo # /tmp/tmpu80Elu/image.h: 615

_ProfileInfo = struct__ProfileInfo # /tmp/tmpu80Elu/image.h: 627

_RectangleInfo = struct__RectangleInfo # /tmp/tmpu80Elu/image.h: 638

_SegmentInfo = struct__SegmentInfo # /tmp/tmpu80Elu/image.h: 647

_ImageInfo = struct__ImageInfo # /tmp/tmpu80Elu/image.h: 976

_MagickInfo = struct__MagickInfo # /tmp/tmpu80Elu/magick.h: 54

_ExportPixelAreaOptions = struct__ExportPixelAreaOptions # /tmp/tmpu80Elu/constitute.h: 105

_ExportPixelAreaInfo = struct__ExportPixelAreaInfo # /tmp/tmpu80Elu/constitute.h: 115

_ImportPixelAreaOptions = struct__ImportPixelAreaOptions # /tmp/tmpu80Elu/constitute.h: 137

_ImportPixelAreaInfo = struct__ImportPixelAreaInfo # /tmp/tmpu80Elu/constitute.h: 147

_DelegateInfo = struct__DelegateInfo # /tmp/tmpu80Elu/delegate.h: 29

# No inserted files

