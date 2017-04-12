# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore


class Separator(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Separator, self).__init__(parent)
        main_layout = QtGui.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        frame = QtGui.QFrame()
        frame.setFrameStyle(QtGui.QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111}')
        main_layout.addWidget(frame)
