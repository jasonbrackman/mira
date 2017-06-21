# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class AddressBookModel(QAbstractItemModel):
    def __init__(self, root_node=None, parent=None):
        super(AddressBookModel, self).__init__(parent)
        self.root_node = root_node

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.root_node

    def rowCount(self, parent):
        parent_node = self.getNode(parent)
        return parent_node.childCount()

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            if index.column() == 0 and node.node_type == "group":
                return node.name()
            if index.column() == 1 and node.node_type == "user":
                return node.name()

    def setData(self, index, value, role):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == Qt.EditRole:
            if index.column() == 0:
                node.setName(value)
                return True
        return False

    def headerData(self, section, orientation, role):
        header_list = ["group", "user"]
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return header_list[section]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def parent(self, index):
        node = self.getNode(index)
        parent_node = node.parent()
        if parent_node == self.root_node:
            return QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        parent_node = self.getNode(parent)
        child_item = parent_node.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()


class LeafFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super(LeafFilterProxyModel, self).__init__()
        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterKeyColumn(-1)

    def filterAcceptsRow(self, row_num, source_parent):
        if self.filter_accepts_row_itself(row_num, source_parent):
            return True
        if self.filter_accepts_any_parent(source_parent):
            return True
        return self.has_accepted_children(row_num, source_parent)

    def filter_accepts_row_itself(self, row_num, parent):
        return super(LeafFilterProxyModel, self).filterAcceptsRow(row_num, parent)

    def filter_accepts_any_parent(self, parent):
        while parent.isValid():
            if self.filter_accepts_row_itself(parent.row(), parent.parent()):
                return True
            parent = parent.parent()
        return False

    def has_accepted_children(self, row_num, parent):
        model = self.sourceModel()
        source_index = model.index(row_num, 0, parent)
        children_count = model.rowCount(source_index)
        for i in xrange(children_count):
            if self.filterAcceptsRow(i, source_index):
                return True
        return False
