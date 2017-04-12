# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore


class Node(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._children = list()
        self._parent = parent
        if parent:
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent:
            return self._parent._children.index(self)

    def isValid(self):
        return False


class IDNode(Node):
    def __init__(self, name, parent=None):
        super(IDNode, self).__init__(name, parent)

    @property
    def node_type(self):
        return "id"


class ContentNode(Node):
    def __init__(self, name, parent=None):
        super(ContentNode, self).__init__(name, parent)
        self.status = "approve"
        self.date = "2016-10-14"
        self.description = "great work!"

    @property
    def node_type(self):
        return "content"


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, root_node=None, parent=None):
        super(TreeModel, self).__init__(parent)
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
        return 5

    def data(self, index, role):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0 and node.node_type == "id":
                return node.name()
            if index.column() == 1 and node.node_type == "content":
                return node.name()
            if index.column() == 2 and node.node_type == "content":
                return node.status
            if index.column() == 3 and node.node_type == "content":
                return node.date
            if index.column() == 4 and node.node_type == "content":
                return node.description

    def setData(self, index, value, role):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == QtCore.Qt.EditRole:
            if index.column() == 0:
                node.setName(value)
                return True
        return False

    def headerData(self, section, orientation, role):
        header_list = ["id", "people", "status", "date", "description"]
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return header_list[section]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def parent(self, index):
        node = self.getNode(index)
        parent_node = node.parent()
        if parent_node == self.root_node:
            return QtCore.QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        parent_node = self.getNode(parent)
        child_item = parent_node.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()


class UserDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        super(UserDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == 4:
            text_edit = QtGui.QTextEdit(parent)
            text_edit.setAutoFillBackground(True)
            text_edit.setStyleSheet("background-color: #00FF00;")
            return text_edit
        else:
            return QtGui.QItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        value = index.data()
        if value:
            editor.setText(value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class LeafFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self):
        super(LeafFilterProxyModel, self).__init__()
        self.setFilterKeyColumn(1)
        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

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


class TreeDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TreeDialog, self).__init__(parent)
        self.resize(600, 300)
        main_layout = QtGui.QVBoxLayout(self)
        self.filter_le = QtGui.QLineEdit()
        main_layout.addWidget(self.filter_le)
        self.tree_view = QtGui.QTreeView()
        main_layout.addWidget(self.tree_view)

        self.root_node = Node("kaka")
        id_node1 = IDNode("103", self.root_node)
        id_node2 = IDNode("105", self.root_node)
        content_node = ContentNode("heshuai", id_node1)
        content_node = ContentNode("zhaopeng", id_node2)

        self.model = TreeModel(self.root_node, self)
        self.proxy_model = LeafFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.tree_view.setModel(self.proxy_model)
        self.tree_view.expandAll()

        self.filter_le.textChanged.connect(self.proxy_model.setFilterRegExp)

        selction_mode = self.tree_view.selectionModel()
        selction_mode.selectionChanged.connect(self.do_test)

        delegate = UserDelegate(self.tree_view)
        self.tree_view.setItemDelegate(delegate)

        root_index = self.tree_view.rootIndex()
        for i in xrange(self.proxy_model.rowCount(root_index)):
            parent_index = self.proxy_model.index(i, 0, root_index)
            src_index = self.proxy_model.mapToSource(parent_index)
            node = src_index.internalPointer()
            if node.node_type == "id":
                for j in xrange(node.childCount()):
                    child_index = self.model.index(j, 4, src_index)
                    self.tree_view.openPersistentEditor(child_index)

    def do_test(self, selected, deselected):
        indexes = selected.indexes()
        if not indexes:
            return
        index = indexes[0]
        index = self.proxy_model.mapToSource(index)
        node = index.internalPointer()
        print node.name()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    td = TreeDialog()
    td.show()
    sys.exit(app.exec_())
