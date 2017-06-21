# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
from miraLibs.pipeLibs.pipeMaya import get_asset_names, export_model_abc
from miraLibs.mayaLibs import get_scene_name
from miraLibs.mayaLibs import get_maya_win
import single_publish_ui
reload(single_publish_ui)


class PublishModel(QAbstractTableModel):
    def __init__(self, arg=[], headers=[], parent=None):
        super(PublishModel, self).__init__(parent)
        self.arg = arg
        self.headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self.arg)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self.arg[row][column]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]


class PublishDelegate(QItemDelegate):
    clicked = Signal(QModelIndex)

    def __init__(self, parent=None):
        super(PublishDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        btn = QPushButton("Publish", parent)
        btn.index = index
        btn.clicked.connect(self.send_index)
        return btn

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def send_index(self):
        self.clicked.emit(self.sender().index)


class SinglePublish(single_publish_ui.SinglePublishUI):
    def __init__(self, parent=None):
        super(SinglePublish, self).__init__(parent)
        self.name = "Single Publish"
        self.setObjectName(self.name)
        self.setWindowTitle(self.name)
        self.set_model()
        self.set_delegate()
        self.set_signals()

    def set_model(self):
        self.table_view.setSortingEnabled(True)
        self.table_view.verticalHeader().hide()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(0)
        self.table_view.setModel(self.proxy_model)
        headers = ["Assets", "Publish"]
        assets = get_asset_names.get_asset_names(False)
        model_data = [[asset.name(), ""] for asset in assets] if assets else []
        self.data_model = PublishModel(model_data, headers)
        self.proxy_model.setSourceModel(self.data_model)
        self.table_view.resizeColumnToContents(0)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.filter_le.textChanged.connect(self.set_filter)

    def set_delegate(self):
        delegate = PublishDelegate(self)
        delegate.clicked.connect(self.do_publish)
        self.table_view.setItemDelegateForColumn(1, delegate)
        self.show_delegate()

    def show_delegate(self):
        for i in xrange(self.proxy_model.rowCount()):
            self.table_view.openPersistentEditor(self.proxy_model.index(i, 1))

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
        selected_assets = list()
        for row in selected_rows:
            asset_full_name = self.data_model.index(row, 0).data()
            selected_assets.append(asset_full_name)
        return selected_assets

    def select_model(self):
        mc.select(clear=1)
        selected_assets = self.get_selected_assets()
        if not selected_assets:
            return
        for asset in selected_assets:
            mc.select(asset, add=1)

    def do_publish(self, index):
        asset_name = self.data_model.index(index.row(), 0).data()
        scene_name = get_scene_name.get_scene_name()
        try:
            export_model_abc.export_model_abc(scene_name, False, asset_name)
            QMessageBox.information(self, "Warming Tip", "Export abc done.")
        except Exception as e:
            print str(e)
            QMessageBox.critical(self, "Error Info", "Export abc fail.")


def main():
    if mc.window("Single Publish", q=1, ex=1):
        mc.deleteUI("Single Publish")
    sp = SinglePublish(get_maya_win.get_maya_win("PySide"))
    sp.show()
