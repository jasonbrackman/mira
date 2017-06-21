# -*- coding: utf-8 -*-
import maya.cmds as mc
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import gpu_to_mdl_ui
reload(gpu_to_mdl_ui)
from miraLibs.mayaLibs import get_maya_win, create_reference


class GpuNode(object):
    def __init__(self, name=None):
        self.base_attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
        self.name = name
        self.parent = None
        self.attr = None
        self.mdl_path = None
        self.shd_path = None

    def get_attr_dict(self):
        attr_dict = dict()
        if mc.nodeType(self.name) == "transform":
            for attr in self.base_attrs:
                value = mc.getAttr("%s.%s" % (self.name, attr))
                attr_dict[attr] = value
        return attr_dict

    def get_parent(self):
        parent = mc.listRelatives(self.name, p=1)
        if parent:
            return parent[0]

    def parse(self):
        self.parent = self.get_parent()
        self.attr = self.get_attr_dict()
        self.mdl_path = mc.getAttr("%s.mdl_path" % self.name)
        self.shd_path = mc.getAttr("%s.shd_path" % self.name)


class GpuModel(QAbstractTableModel):
    def __init__(self, arg=[], headers=[], parent=None):
        super(GpuModel, self).__init__(parent)
        self.arg = arg
        self.headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self.arg)

    def columnCount(self, parent=QModelIndex()):
        return 3

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self.arg[row][column]

    def setData(self, index, value, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.arg[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]


class ComboDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ComboDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == 1:
            combo = QComboBox(parent)
            combo.addItems(["mdl", "shd"])
            combo.currentIndexChanged.connect(self.onCurrentIndexChanged)
            return combo

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        source_index = model.mapToSource(index)
        model.sourceModel().setData(source_index, value, Qt.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def onCurrentIndexChanged(self, index):
        self.commitData.emit(self.sender())


class ReplaceDelegate(QItemDelegate):
    clicked = Signal(QModelIndex)

    def __init__(self, parent=None):
        super(ReplaceDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        btn = QPushButton("Replace", parent)
        btn.index = index
        btn.clicked.connect(self.send_index)
        return btn

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def send_index(self):
        self.clicked.emit(self.sender().index)


class Maya(object):

    @staticmethod
    def get_gpu():
        gpu_shape = mc.ls(type="gpuCache")
        if not gpu_shape:
            return
        gpu_node = [mc.listRelatives(gpu, p=1)[0] for gpu in gpu_shape]
        return gpu_node

    @staticmethod
    def clear_selection():
        mc.select(clear=1)

    @staticmethod
    def select_gpu(gpu):
        mc.select(gpu, r=1)

    @staticmethod
    def build_group(node, parent):
        try:
            mc.parent(node, parent)
        except:pass

    @staticmethod
    def set_attr(node, new_node):
        for attr in node.attr:
            mc.setAttr("%s.%s" % (new_node, attr), node.attr[attr])

    def replace_gpu_to_shd(self, gpu_node, path_type):
        if path_type == "mdl":
            path = gpu_node.mdl_path
        else:
            path = gpu_node.shd_path
        namespace = gpu_node.name
        group_name = create_reference.create_reference(path, namespace_name=namespace, allow_repeat=True, get_group=True)
        print group_name
        self.build_group(group_name, gpu_node.parent)
        self.set_attr(gpu_node, group_name)


class GpuMdl(gpu_to_mdl_ui.GpuToMdlUI):
    def __init__(self, parent=None):
        super(GpuMdl, self).__init__(parent)
        self.setObjectName("GPU to model")
        self.setWindowTitle("GPU to model")
        self.maya = Maya()
        self.set_model()
        self.set_delegate()
        self.set_signals()

    def set_model(self):
        self.table_view.setSortingEnabled(True)
        self.table_view.verticalHeader().hide()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(0)
        self.table_view.setModel(self.proxy_model)
        headers = ["gpu", "mdl/shd", "Replace"]
        gpu_node = self.maya.get_gpu()
        model_data = [[gpu, "mdl", None] for gpu in gpu_node] if gpu_node else []
        self.data_model = GpuModel(model_data, headers)
        self.proxy_model.setSourceModel(self.data_model)
        self.table_view.resizeColumnToContents(0)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.filter_le.textChanged.connect(self.set_filter)
        column_width_list = [200, 100, 100]
        for column in range(3):
            self.table_view.setColumnWidth(column, column_width_list[column])

    def set_delegate(self):
        delegate = ComboDelegate(self)
        self.table_view.setItemDelegateForColumn(1, delegate)
        replace_delegate = ReplaceDelegate(self)
        replace_delegate.clicked.connect(self.do_replace)
        self.table_view.setItemDelegateForColumn(2, replace_delegate)
        self.show_delegate()

    def show_delegate(self):
        for i in xrange(self.proxy_model.rowCount()):
            self.table_view.openPersistentEditor(self.proxy_model.index(i, 1))
            self.table_view.openPersistentEditor(self.proxy_model.index(i, 2))

    def set_filter(self, value):
        self.proxy_model.setFilterRegExp(value)
        self.show_delegate()

    def set_signals(self):
        selection = self.table_view.selectionModel()
        if selection:
            selection.selectionChanged.connect(self.select_model)
        self.table_view.clicked.connect(self.select_model)
        self.update_btn.clicked.connect(self.do_update)

    def do_update(self):
        self.set_model()
        self.set_delegate()

    def get_selected_assets(self):
        selected_indexes = self.table_view.selectedIndexes()
        if not selected_indexes:
            return
        selected_rows = list(set([self.proxy_model.mapToSource(i).row() for i in selected_indexes]))
        selected_gpu = list()
        for row in selected_rows:
            gpu_name = self.data_model.index(row, 0).data()
            selected_gpu.append(gpu_name)
        return selected_gpu

    def select_model(self):
        self.maya.clear_selection()
        selected_gpu = self.get_selected_assets()
        if not selected_gpu:
            return
        self.maya.select_gpu(selected_gpu)

    def do_replace(self, index):
        gpu_name = self.data_model.index(index.row(), 0).data()
        mdl_or_shd = self.data_model.index(index.row(), 1).data()
        print gpu_name, mdl_or_shd
        gpu_node = GpuNode(gpu_name)
        gpu_node.parse()
        self.maya.replace_gpu_to_shd(gpu_node, mdl_or_shd)


def main():
    if mc.window("GPU to model", q=1, ex=1):
        mc.deleteUI("GPU to model")
    sp = GpuMdl(get_maya_win.get_maya_win("PySide"))
    sp.show()
