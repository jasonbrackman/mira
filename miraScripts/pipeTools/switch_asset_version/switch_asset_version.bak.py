# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
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


class AssetTreeModel(QtCore.QAbstractItemModel):
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
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0 and node.node_type == "asset_type":
                return node.name
            if index.column() == 1 and node.node_type == "asset":
                return node.name
            if index.column() == 3 and node.node_type == "asset":
                return node.dst_path
        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 2 and node.node_type == "asset":
                pix_map_path = node.thumbnail_path
                pix_map = QtGui.QPixmap(pix_map_path)
                scaled = pix_map.scaled(QtCore.QSize(100, 100), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                return scaled
        elif role == QtCore.Qt.SizeHintRole:
            if node.node_type == "asset_type":
                return QtCore.QSize(20, 20)

    def setData(self, index, value, role):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == QtCore.Qt.EditRole:
            if index.column() == 0:
                node.name = value
                return True
        return False

    def headerData(self, section, orientation, role):
        header_list = ["Asset Type", "Asset Name", "Thumbnail", "Destination Path"]
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


class AssetDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        super(AssetDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        print index.model().index(index.row(), 1, index.parent()).data()
        if index.column() == 3:
            line_edit = QtGui.QLineEdit(parent)
            line_edit.setStyleSheet("background: #FF0000;color:#FF0000;")
            return line_edit
        else:
            return QtGui.QItemDelegate.createEditor(self, parent, option, index)
        # tree_view = QtGui.QTreeView(parent)
        # return tree_view

    def setEditorData(self, editor, index):
        if index.column() == 3:
            value = index.data()
            if value:
                # system_model = QtGui.QFileSystemModel()
                # system_model.setRootPath(value)
                # editor.setModel(system_model)
                editor.setText(value)
        else:
            QtGui.QItemDelegate.setEditorData(self, editor, index)

    def updateEditorGeometry(self, editor, option, index):
        if index.column() == 3:
            editor.setGeometry(option.rect)
        else:
            QtGui.QItemDelegate.updateEditorGeometry(self, editor, option, index)


class LeafFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self):
        super(LeafFilterProxyModel, self).__init__()
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


class ReplaceAsset(ui.ReplaceAssetUI):
    def __init__(self, parent=None):
        super(ReplaceAsset, self).__init__(parent)
        self.init()
        self.do_refresh()
        self.set_signals()

    def init(self):
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tree_view.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

    def set_signals(self):
        self.replace_btn.clicked.connect(self.do_replace)
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
            model = QtGui.QStandardItemModel()
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
        self.proxy_model = LeafFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.tree_view.setModel(self.proxy_model)
        self.tree_view.expandAll()
        self.tree_view.resizeColumnToContents(1)
        self.filter_le.textChanged.connect(self.filter_name)

        # selection = self.tree_view.selectionModel()
        # if selection:
        #     selection.selectionChanged.connect(self.select_model)

    def set_delegate(self):
        delegate = AssetDelegate(self.tree_view)
        self.tree_view.setItemDelegateForColumn(3, delegate)

    def show_delegate(self):
        root_index = self.tree_view.rootIndex()
        for i in xrange(self.proxy_model.rowCount(root_index)):
            parent_index = self.proxy_model.index(i, 0, root_index)
            src_index = self.proxy_model.mapToSource(parent_index)
            node = src_index.internalPointer()
            if node.node_type == "asset_type":
                for j in xrange(node.childCount()):
                    child_index = self.model.index(j, 3, src_index)
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
            source_index = self.proxy_model.mapToSource(index)
            node = source_index.internalPointer()
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

    def do_replace(self):
        selected = self.get_selected()
        if not selected:
            return
        progress_dialog = QtGui.QProgressDialog('Replacing...', 'Cancel', 0, len(selected))
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.setMinimumWidth(400)
        progress_dialog.show()
        for index, sel in enumerate(selected):
            progress_dialog.setValue(index)
            mayaOpt.replace(*sel)
            if progress_dialog.wasCanceled():
                break
        self.set_model()


def main():
    import maya.cmds as mc
    if mc.window("Replace Asset Version", q=1, ex=1):
        mc.deleteUI("Replace Asset Version")
    ra = ReplaceAsset(get_maya_win.get_maya_win("PySide"))
    ra.show()
