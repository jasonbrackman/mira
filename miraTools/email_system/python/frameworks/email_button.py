# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from ..libs import get_icon_dir


BUTTON_STYLESHEET = "QPushButton{" \
                    "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, " \
                    "stop: 0 #c7eff5, stop: 0.5 #eafafc, stop: 1.0 #c7eff5); " \
                    "border-radius: 1px;}" \
                    "QPushButton::hover{" \
                    "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1," \
                    "stop: 0 #e4fcff, stop: 0.5 #eafafc,stop: 1.0 #e4fcff);" \
                    "border-color: #AAAAAA; border-width: 1px; border-style: outset;padding: 1px;}" \
                    "QPushButton::pressed{" \
                    "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1," \
                    "stop: 0 #c7eff5, stop: 0.5 #eafafc,stop: 1.0 #c7eff5);}"


class EmailButton(QPushButton):
    def __init__(self, name=None, text=None, parent=None):
        super(EmailButton, self).__init__(parent)
        self.name = name
        self.text = " %s" % text
        icon_dir = get_icon_dir.get_icon_dir()
        icon_path = os.path.join(icon_dir, "%s.png" % self.name)
        icon = QIcon(icon_path)
        self.setIcon(icon)
        self.setText(self.text)
        self.setMinimumSize(80, 30)
        self.setIconSize(QSize(25, 25))
        self.setStyleSheet(BUTTON_STYLESHEET)

