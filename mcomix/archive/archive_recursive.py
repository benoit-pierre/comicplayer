# -*- coding: utf-8 -*-

""" Class for transparently handling an archive containing sub-archives. """

from mcomix.archive import archive_base
from mcomix import archive_tools
from mcomix import log

import os

class RecursiveArchive(archive_base.BaseArchive):

    def __init__(self, archive, destination_dir):
        self._main_archive = archive
        self._destination_dir = destination_dir
        self._archive_list = []
        # Map entry name to its archive+name.
        self._entry_mapping = {}
        # Map archive to its root.
        self._archive_root = {}
        self._contents_listed = False
        self._contents = []
        # Assume concurrent extractions are not supported.
        self.support_concurrent_extractions = False

    def _iter_contents(self, archive, root=None):
        self._archive_list.append(archive)
        self._archive_root[archive] = root
        supported_archive_regexp = archive_tools.get_supported_archive_regex()
        for f in archive.iter_contents():
            if supported_archive_regexp.search(f):
                # Extract sub-archive.
                destination_dir = os.path.join(self._destination_dir, 'sub-archives')
                if root is not None:
                    destination_dir = os.path.join(destination_dir, root)
                archive.extract(f, destination_dir)
                # And open it and list its contents.
                sub_archive_path = os.path.join(destination_dir, f)
                # Ignore directories!
                if os.path.isdir(sub_archive_path):
                    continue
                sub_archive = archive_tools.get_archive_handler(sub_archive_path)
                if sub_archive is None:
                    log.warning('Non-supported archive format: %s' %
                                os.path.basename(sub_archive_path))
                    continue
                sub_root = f
                if root is not None:
                    sub_root = os.path.join(root, sub_root)
                for name in self._iter_contents(sub_archive, sub_root):
                    yield name
            else:
                name = f
                if root is not None:
                    name = os.path.join(root, name)
                self._entry_mapping[name] = (archive, f)
                yield name

    def _check_concurrent_extraction_support(self):
        supported = True
        # We need all archives to support concurrent extractions.
        for archive in self._archive_list:
            if not archive.support_concurrent_extractions:
                supported = False
                break
        self.support_concurrent_extractions = supported

    def iter_contents(self):
        if self._contents_listed:
            for f in self._contents:
                yield f
            return
        self._contents = []
        for f in self._iter_contents(self._main_archive):
            self._contents.append(f)
            yield f
        self._contents_listed = True
        # We can now check if concurrent extractions are really supported.
        self._check_concurrent_extraction_support()

    def list_contents(self):
        if self._contents_listed:
            return self._contents
        return [f for f in self.iter_contents()]

    def extract(self, filename, destination_dir):
        if not self._contents_listed:
            self.list_contents()
        archive, name = self._entry_mapping[filename]
        root = self._archive_root[archive]
        if root is not None:
            destination_dir = os.path.join(destination_dir, root)
        archive.extract(name, destination_dir)

    def iter_extract(self, entries, destination_dir):
        if not self._contents_listed:
            self.list_contents()
        # Unfortunately we can't just rely on BaseArchive default
        # implementation if solid archives are to be correctly supported:
        # we need to call iter_extract (not extract) for each archive ourselves.
        wanted = set(entries)
        for archive in self._archive_list:
            archive_wanted = filter(lambda f: archive == self._entry_mapping[f][0], wanted)
            if 0 == len(archive_wanted):
                continue
            root = self._archive_root[archive]
            archive_destination_dir = destination_dir
            if root is not None:
                archive_destination_dir = os.path.join(destination_dir, root)
            for f in archive.iter_extract(list(archive_wanted), archive_destination_dir):
                yield f
            wanted -= set(archive_wanted)
            if 0 == len(wanted):
                break

    def is_solid(self):
        if not self._contents_listed:
            self.list_contents()
        # We're solid if at least one archive is solid.
        for archive in self._archive_list:
            if archive.is_solid():
                return True
        return False

    def close(self):
        for archive in self._archive_list:
            archive.close()

