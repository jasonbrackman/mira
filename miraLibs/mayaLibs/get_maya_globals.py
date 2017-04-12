# -*- coding: utf-8 -*-
import logging
from PySide import QtGui


class MayaGlobals(object):
    def __init__(self):
        self.__dict = dict()

    def add(self, *args, **kwargs):
        for key in args:
            if key not in self.__dict:
                self.__dict[key] = None
        for key in kwargs:
            self.__dict[key] = kwargs[key]

    def update(self, **kwargs):
        for key in kwargs:
            if key not in self.__dict:
                logging.warning("No var name match %s,please add it first" % key)
                continue
            self.__dict[key] = kwargs[key]

    def get(self, key):
        if key not in self.__dict:
            logging.error("No var name match %s,please add it first" % key)
            raise ValueError("No var name match %s,please add it first" % key)
        return self.__dict[key]

    def pop(self, key):
        return self.__dict.pop(key)

    def keys(self):
        return self.__dict.keys()

    def exists(self, key):
        return key in self.__dict.keys()


def get_maya_globals():
    maya_app = QtGui.qApp
    if not hasattr(maya_app, "globals"):
        maya_app.globals = MayaGlobals()
    return maya_app.globals

if __name__ == "__main__":
    pass
