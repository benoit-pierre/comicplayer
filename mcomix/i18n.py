""" i18n.py - Encoding and translation handler."""

import sys
import locale

try:
    import chardet
except ImportError:
    chardet = None

def to_unicode(string):
    """Convert <string> to unicode. First try the default filesystem
    encoding, and then fall back on some common encodings.
    """
    if isinstance(string, unicode):
        return string

    # Try chardet heuristic
    if chardet:
        probable_encoding = chardet.detect(string)['encoding'] or \
            locale.getpreferredencoding() # Fallback if chardet detection fails
    else:
        probable_encoding = locale.getpreferredencoding()

    for encoding in (
        probable_encoding,
        sys.getfilesystemencoding(),
        'utf-8',
        'latin-1'):

        try:
            ustring = unicode(string, encoding)
            return ustring

        except (UnicodeError, LookupError):
            pass

    return string.decode('utf-8', 'replace')

def to_utf8(string):
    """ Helper function that converts unicode objects to UTF-8 encoded
    strings. Non-unicode strings are assumed to be already encoded
    and returned as-is. """

    if isinstance(string, unicode):
        return string.encode('utf-8')
    else:
        return string

# vim: expandtab:sw=4:ts=4
