# -*- coding: utf-8 -*-
import os
from PySide import QtGui, QtCore
from utility.get_icon_dir import get_icon_dir


class ToolButton(QtGui.QToolButton):
    def __init__(self, name=None, parent=None):
        super(ToolButton, self).__init__(parent)
        self.__name = name
        self.__icon_dir = get_icon_dir()
        icon_path = os.path.join(self.__icon_dir, "%s.png" % self.__name)
        self.setIcon(QtGui.QIcon(icon_path))


class ToolWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ToolWidget, self).__init__(parent)
        self.setAutoFillBackground(True)
        main_layout = QtGui.QHBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.add_btn = ToolButton("add", self)
        self.remove_btn = ToolButton("remove", self)
        self.insert_btn = ToolButton("insert", self)
        self.clear_btn = ToolButton("clear", self)
        main_layout.addStretch()
        main_layout.addWidget(self.add_btn)
        main_layout.addWidget(self.remove_btn)
        main_layout.addWidget(self.insert_btn)
        main_layout.addWidget(self.clear_btn)
