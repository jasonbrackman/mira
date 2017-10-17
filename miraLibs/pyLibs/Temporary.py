# -*- coding: utf-8 -*-
import os
import logging
import warnings
from tempfile import mkdtemp, mktemp


class Temporary(object):
    """
    Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For

    Examples:
    >>> with TemporaryDirectory() as tmpdir:
    >>>     ...
    Upon exiting the context, the directory and everything contained
    in it are removed.
    """

    def __init__(self, suffix="", prefix="tmp", dir_=None, mode="mkdtemp"):
        self._closed = False
        self.name = None  # Handle mkdtemp raising an exception
        if mode == "mkdtemp":
            self.name = mkdtemp(suffix, prefix, dir_)
        elif mode == "mktemp":
            self.name = mktemp(suffix, prefix, dir_)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def cleanup(self, _warn=False):
        if self.name and not self._closed:
            try:
                self._rmtree(self.name)
            except (TypeError, AttributeError) as ex:
                # Issue #10188: Emit a warning on
                # if the directory could not be cleaned
                # up due to missing globals
                if "None" not in str(ex):
                    logging.info("ERROR: {!r} while cleaning up {!r}".format(ex, self, ))
                    raise
                return
            self._closed = True
            if _warn:
                logging.warning("Implicitly cleaning up {!r}".format(self))

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def __del__(self):
        # Issue a ResourceWarning if implicit cleanup needed
        self.cleanup(_warn=True)

    # XXX (ncoghlan): The following code attempts to make
    # this class tolerant of the module nulling out process
    # that happens during CPython interpreter shutdown
    # Alas, it doesn't actually manage it. See issue #10188
    _listdir = staticmethod(os.listdir)
    _path_join = staticmethod(os.path.join)
    _isdir = staticmethod(os.path.isdir)
    _islink = staticmethod(os.path.islink)
    _remove = staticmethod(os.remove)
    _rmdir = staticmethod(os.rmdir)
    _warn = warnings.warn

    def _rmtree(self, path):
        # Essentially a stripped down version of shutil.rmtree.  We can't
        # use globals because they may be None'ed out at shutdown.
        for name in self._listdir(path):
            fullname = self._path_join(path, name)
            try:
                isdir = self._isdir(fullname) and not self._islink(fullname)
            except OSError:
                isdir = False
            if isdir:
                self._rmtree(fullname)
            else:
                try:
                    self._remove(fullname)
                except OSError:
                    pass
        try:
            self._rmdir(path)
        except OSError:
            pass