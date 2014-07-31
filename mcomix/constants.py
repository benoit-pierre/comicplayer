# -*- coding: utf-8 -*-
"""constants.py - Miscellaneous constants."""

import re

ZIP, RAR, TAR, GZIP, BZIP2, PDF, SEVENZIP, LHA, ZIP_EXTERNAL = range(9)

SUPPORTED_IMAGE_REGEX = re.compile(r'\.(jpg|jpeg|png|gif|tif|tiff|bmp|ppm|pgm|pbm)\s*$', re.I)

ZIP_FORMATS = (
        ('application/x-zip', 'application/zip', 'application/x-zip-compressed', 'application/x-cbz'),
        ('*.zip', '*.cbz'))
RAR_FORMATS = (
        ('application/x-rar', 'application/x-cbr'),
        ('*.rar', '*.cbr'))
TAR_FORMATS = (
        ('application/x-tar', 'application/x-gzip', 'application/x-bzip2', 'application/x-cbt'),
        ('*.tar', '*.gz', '*.bz2', '*.bzip2', '*.cbt'))
SZIP_FORMATS = (
        ('application/x-7z-compressed', 'application/x-cb7'),
        ('*.7z', '*.cb7', '*.xz', '*.lzma'))
LHA_FORMATS = (
        ('application/x-lzh', 'application/x-lha', 'application/x-lzh-compressed'),
        ('*.lha', '*.lzh'))
PDF_FORMATS = (
        ('application/pdf',),
        ('*.pdf',))

# vim: expandtab:sw=4:ts=4
