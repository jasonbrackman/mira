# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class Separator(QWidget):
    def __init__(self, parent=None):
        super(Separator, self).__init__(parent)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        frame = QFrame()
        frame.setFrameStyle(QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111}')
        main_layout.addWidget(frame)
