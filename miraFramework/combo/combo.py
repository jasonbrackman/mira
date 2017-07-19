# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *


class ComboModel(QAbstractListModel):
    def __init__(self, model_data=None, parent=None):
        super(ComboModel, self).__init__(parent)
        self.model_data = model_data
        self.parent = parent

    def rowCount(self, parent):
        return len(self.model_data)

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        row = index.row()
        if role == Qt.DisplayRole:
            return self.model_data[row]
        elif role == Qt.SizeHintRole:
            return QSize(self.parent.width(), 25)


class CombBox(QComboBox):
    def __init__(self, model_data, parent=None):
        super(CombBox, self).__init__(parent)
        self.__model_data = model_data
        self.model = ComboModel(self.__model_data)
        self.setModel(self.model)
