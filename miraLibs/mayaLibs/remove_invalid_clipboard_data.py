# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


def remove_invalid_clipboard_data():
    qApp = QApplication.instance()
    oldMimeData = qApp.clipboard().mimeData()
    newMimeData = QMimeData()
    for format in oldMimeData.formats():
        if 'text/uri-list' in format:
            continue
        data = oldMimeData.data(format)
        newMimeData.setData(format, data)
    clipboard = qApp.clipboard()
    clipboard.blockSignals(True)
    clipboard.setMimeData(newMimeData)
    clipboard.blockSignals(False)
    qApp.clipboard().dataChanged.connect(remove_invalid_clipboard_data)