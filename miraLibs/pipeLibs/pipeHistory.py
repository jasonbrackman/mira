# -*- coding: utf-8 -*-
from PySide import QtCore


def get(content):
    settings = QtCore.QSettings("Mira", "History")
    return settings.value(content)


def set(key, value):
    settings = QtCore.QSettings("Mira", "History")
    settings.setValue(key, value)
