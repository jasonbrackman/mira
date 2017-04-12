# -*- coding: utf-8 -*-
import os
import clear_dir
import get_children_file
import start_file


class Path(object):
    def __init__(self, path):
        self.path = path.replace("\\", "/")
        if not self.path:
            raise IOError("Path is None")

    @staticmethod
    def regular_path(p):
        return p.replace("\\", "/")

    def regular(self):
        return self.regular_path(self.path)

    def dirname(self):
        dir_name = os.path.dirname(self.path)
        return self.regular_path(dir_name)

    def basename(self):
        return os.path.basename(self.regular())

    def isfile(self):
        return os.path.isfile(self.regular())

    def isdir(self):
        return os.path.isdir(self.regular())

    def makedirs(self):
        dirname = self.regular()
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def rename(self, new_name):
        os.rename(self.regular(), new_name)

    def listdir(self):
        if self.isfile():
            return
        elif self.isdir():
            return os.listdir(self.regular())
        else:
            return

    def children(self, ext=None):
        if self.isfile():
            return
        elif self.isdir():
            get_children_file.get_children_file(self.regular(), ext)

    def remove(self):
        if self.isfile():
            os.remove(self.regular())
        elif self.isdir():
            clear_dir.clear_dir(self.regular())
        else:
            return

    def startfile(self):
        start_file.start_file(self.regular())
