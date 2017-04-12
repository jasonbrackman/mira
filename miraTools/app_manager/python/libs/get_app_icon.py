# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore


def get_app_icon(path):
    file_info = QtCore.QFileInfo(path)
    icon_provider = QtGui.QFileIconProvider()
    icon = icon_provider.icon(file_info)
    return icon
