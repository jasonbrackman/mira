# -*- coding: utf-8 -*-
from Qt import QtWidgets
from Qt import QtCore


class BaseUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def create_label(self):
        label = QtWidgets.QLabel()

        pass



class PipelineUI(QtWidgets.QDialog):
    def __init__(self, widget, parent=None):
        if not isinstance(widget, QtWidgets.QWidget):
            raise TypeError("'widget' must be a qt widget object, %s got." % type(widget))
        self.setWindowFlags(QtCore.Qt.Window)

