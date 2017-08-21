# -*- coding: utf-8 -*-
from Qt.QtCore import *


class ListModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.__model_data = model_data

    @property
    def model_data(self):
        return self.__model_data

    @model_data.setter
    def model_data(self, value):
        self.__model_data = value

    def rowCount(self, parent=QModelIndex()):
        return len(self.__model_data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return
        row = index.row()
        if role == Qt.DisplayRole:
            return self.__model_data[row]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class FilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(FilterProxyModel, self).__init__(parent)
        self.name_regexp = QRegExp()
        self.name_regexp.setCaseSensitivity(Qt.CaseInsensitive)
        self.name_regexp.setPatternSyntax(QRegExp.RegExp)

    def filterAcceptsRow(self, source_row, source_parent):
        name_index = self.sourceModel().index(source_row, 0, source_parent)
        item = self.sourceModel().data(name_index)
        if self.name_regexp.isEmpty():
            return True
        else:
            reg_str = "%s%s%s%s%s" % (item.asset_type_sequence, item.asset_name_shot, item.step, item.task, item.status)
            return self.name_regexp.exactMatch(reg_str)

    def set_name_filter(self, regexp):
        regexp = ".*%s.*" % regexp if regexp else ""
        self.name_regexp.setPattern(regexp)
        self.invalidateFilter()
