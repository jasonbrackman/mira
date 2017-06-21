# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import ui
reload(ui)
import mayaOpt
reload(mayaOpt)
from miraLibs.mayaLibs import get_maya_win


class Node(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._children = list()
        self._parent = parent
        if parent:
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
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


class AssetTypeNode(Node):
    def __init__(self, name, parent=None):
        super(AssetTypeNode, self).__init__(name, parent)

    @property
    def node_type(self):
        return "asset_type"


class AssetNode(Node):
    def __init__(self, name, thumbnail_path, dst_path, parent=None):
        super(AssetNode, self).__init__(name, parent)
        self.thumbnail_path = thumbnail_path
        self.dst_path = dst_path

    @property
    def node_type(self):
        return "asset"


class AssetTreeModel(QAbstractItemModel):
    def __init__(self, root_node=None, parent=None):
        super(AssetTreeModel, self).__init__(parent)
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
        return 4

    def data(self, index, role):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            if index.column() == 0 and node.node_type == "asset_type":
                return node.name
            if index.column() == 1 and node.node_type == "asset":
                return node.name
            if index.column() == 3 and node.node_type == "asset":
                return node.dst_path
        elif role == Qt.DecorationRole:
            if index.column() == 2 and node.node_type == "asset":
                pix_map_path = node.thumbnail_path
                pix_map = QPixmap(pix_map_path)
                scaled = pix_map.scaled(QSize(100, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                return scaled
        elif role == Qt.SizeHintRole:
            if node.node_type == "asset_type":
                return QSize(20, 20)

    def setData(self, index, value, role):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == Qt.EditRole:
            if index.column() == 0:
                node.name = value
                return True
        return False

    def headerData(self, section, orientation, role):
        header_list = ["Asset Type", "Asset Name", "Thumbnail", "Destination Path"]
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


class ListWidget(QListWidget):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clearSelection()
        super(ListWidget, self).mousePressEvent(event)


class AssetDelegate(QItemDelegate):
    double_clicked_signal = Signal(QListWidgetItem)

    def __init__(self, parent=None):
        super(AssetDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == 3:
            list_widget = ListWidget(parent)
            list_widget.setMaximumHeight(100)
            list_widget.setFocusPolicy(Qt.NoFocus)
            list_widget.setAutoFillBackground(True)
            list_widget.itemDoubleClicked.connect(self.emit_double_clicked)
            return list_widget
        else:
            return QItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        if index.column() == 3:
            value = index.data()
            if value:
                for i in os.listdir(value):
                    if not os.path.splitext(i)[-1] in [".mb", ".ma"]:
                        continue
                    path = os.path.join(value, i).replace("\\", "/")
                    item = QListWidgetItem(path)
                    item.index = index
                    editor.addItem(item)
        else:
            QItemDelegate.setEditorData(self, editor, index)

    def updateEditorGeometry(self, editor, option, index):
        if index.column() == 3:
            editor.setGeometry(option.rect)
        else:
            QItemDelegate.updateEditorGeometry(self, editor, option, index)

    def sizeHint(self, option, index):
        return QSize(160, 10)

    def emit_double_clicked(self, item):
        self.double_clicked_signal.emit(item)


class ReplaceAsset(ui.ReplaceAssetUI):
    def __init__(self, parent=None):
        super(ReplaceAsset, self).__init__(parent)
        self.init()
        self.do_refresh()
        self.set_signals()

    def init(self):
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setFocusPolicy(Qt.NoFocus)
        self.tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def set_signals(self):
        self.update_btn.clicked.connect(self.do_refresh)

    def do_refresh(self):
        self.set_model()
        try:
            self.set_delegate()
            self.show_delegate()
        except Exception as e:
            print e

    def set_model(self):
        self.root_node = Node("Asset Switch")
        model_data = mayaOpt.get_asset_list()
        if not model_data:
            model = QStandardItemModel()
            self.tree_view.setModel(model)
            return
        asset_type_list = [asset_list[3] for asset_list in model_data]
        asset_type_list = list(set(asset_type_list))
        asset_type_nodes = [AssetTypeNode(asset_type, self.root_node) for asset_type in asset_type_list]
        for asset_list in model_data:
            group_name, thumbnail_path, dst_path, asset_type = asset_list
            parent_node = [node for node in asset_type_nodes if node.name == asset_type][0]
            asset_node = AssetNode(group_name, thumbnail_path, dst_path, parent_node)
        self.model = AssetTreeModel(self.root_node, self)
        self.tree_view.setModel(self.model)
        self.tree_view.expandAll()
        self.tree_view.resizeColumnToContents(1)

        selection = self.tree_view.selectionModel()
        if selection:
            selection.selectionChanged.connect(self.select_model)

    def set_delegate(self):
        delegate = AssetDelegate(self.tree_view)
        delegate.double_clicked_signal.connect(self.do_replace)
        self.tree_view.setItemDelegateForColumn(3, delegate)

    def show_delegate(self):
        root_index = self.tree_view.rootIndex()
        for i in xrange(self.model.rowCount(root_index)):
            parent_index = self.model.index(i, 0, root_index)
            node = parent_index.internalPointer()
            if node.node_type == "asset_type":
                for j in xrange(node.childCount()):
                    child_index = self.model.index(j, 3, parent_index)
                    self.tree_view.openPersistentEditor(child_index)

    def filter_name(self, name):
        self.proxy_model.setFilterKeyColumn(1)
        self.proxy_model.setFilterRegExp(name)
        self.tree_view.expandAll()

    def get_selected(self):
        selected_list = list()
        indexes = self.tree_view.selectedIndexes()
        if not indexes:
            return
        for index in indexes:
            node = index.internalPointer()
            if node.node_type == "asset_type":
                continue
            group_name = node.name
            new_path = node.dst_path
            temp_list = [group_name, new_path]
            if temp_list not in selected_list:
                selected_list.append(temp_list)
        return selected_list

    def select_model(self):
        selected = self.get_selected()
        if not selected:
            return
        if self.select_check.isChecked():
            maya_objects = [sel[0] for sel in selected]
            mayaOpt.select(maya_objects)

    def do_replace(self, item):
        item_index = item.index
        path = item.text()
        model_name = item_index.model().index(item_index.row(), 1, item_index.parent()).data()
        mayaOpt.replace(model_name, path)


def main():
    import maya.cmds as mc
    if mc.window("Replace Asset Version", q=1, ex=1):
        mc.deleteUI("Replace Asset Version")
    ra = ReplaceAsset(get_maya_win.get_maya_win("PySide"))
    ra.show()
