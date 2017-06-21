# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class EmailListModel(QAbstractListModel):
    def __init__(self, arg=[], box=None, parent=None):
        super(EmailListModel, self).__init__(parent)
        self.box = box
        self.arg = arg
        self.clicked_indexes = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.arg)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        email_item = self.arg[row]
        if role == Qt.ToolTipRole:
            return email_item.content.decode("utf-8")
        if role == Qt.DisplayRole:
            return "Title:   %s\nFrom: %s\nDate:  %s" % (email_item.title.decode("utf-8"), email_item.sender, email_item.send_time.decode("utf-8"))
        if self.box == "receiveBox":
            if role == Qt.FontRole:
                font = QFont()
                if not int(email_item.isRead):
                    font.setBold(True)
                else:
                    font.setBold(False)
                if index in self.clicked_indexes:
                    font.setBold(False)
                return font

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRows(self, position, count, value, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for index, i in enumerate(value):
            self.arg.insert(position+index, i)
        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position+count-1)
        for i in range(count):
            value = self.arg[position]
            self.arg.remove(value)
        self.endRemoveRows()
        return True

    def setData(self, index, value, role):
        if role == Qt.FontRole:
            if value:
                role_font = self.data(index, role)
                role_font.setBold(False)
                role_font.setWeight(50)
        self.dataChanged.emit(index, index)
        return True
