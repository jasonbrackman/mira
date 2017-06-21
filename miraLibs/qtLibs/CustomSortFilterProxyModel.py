# -*- coding: utf-8 -*-
import logging
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class CustomSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, columns=[], parent=None):
        super(CustomSortFilterProxyModel, self).__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.columns = columns
        self.regexp_list = []
        if self.columns:
            for column in self.columns:
                regexp_object = QRegExp()
                regexp_object.setCaseSensitivity(Qt.CaseInsensitive)
                regexp_object.setPatternSyntax(QRegExp.RegExp)
                self.regexp_list.append(regexp_object)

    def filterAcceptsRow(self, source_row, source_parent):
        is_empty_list = []
        is_matched_list = []
        if not self.columns:
            return True
        for column_index, column in enumerate(self.columns):
            index = self.sourceModel().index(source_row, column, source_parent)
            value = str(self.sourceModel().data(index))
            is_empty = self.regexp_list[column_index].isEmpty()
            is_empty_list.append(is_empty)
            is_matched = self.regexp_list[column_index].exactMatch(value)
            is_matched_list.append(is_matched)
        if all(is_empty_list):
            return True
        elif any(is_empty_list):
            return any(is_matched_list)
        else:
            return all(is_matched_list)

    def set_filter(self, column, regexp):
        regexp = ".*%s.*" % regexp if regexp else ""
        try:
            column_index = self.columns.index(column)
            self.regexp_list[column_index].setPattern(regexp)
            self.invalidateFilter()
        except Exception as e:
            self.logger.error(str(e))
