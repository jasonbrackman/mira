# -*- coding: utf-8 -*-
import logging
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
import pymel.core as pm
import pipeGlobal
from miraLibs.pipeLibs.pipeMaya import get_asset_names, get_current_project, lgt_assign_shader_deformed
reload(lgt_assign_shader_deformed)
from miraLibs.mayaLibs import get_maya_win, replace_reference
from miraFramework.Filter import Filter
from miraLibs.pyLibs import join_path
from miraLibs.pipeLibs import pipeFile


ASSET_DICT = {"char": "character", "prop": "prop", "env": "environment"}


class AssetTableModel(QAbstractTableModel):
    def __init__(self, arg=[], parent=None):
        super(AssetTableModel, self).__init__(parent)
        self.__arg = arg

    @property
    def arg(self):
        return self.__arg

    @arg.setter
    def arg(self, value):
        self.__arg = value

    def rowCount(self, parent):
        return len(self.__arg)

    def columnCount(self, parent):
        return len(self.__arg[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self.__arg[row][column]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.__arg[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
        header_data = ["Assets", "Shader Version"]
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return header_data[section]


class ComboDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ComboDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == 1:
            combo = QComboBox(parent)
            combo.currentIndexChanged.connect(self.onCurrentIndexChanged)
            return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        source_index = index.model().mapToSource(index)
        value = source_index.data()
        if isinstance(value, list):
            editor.addItems(value)
            model_name_proxy_index = index.model().index(index.row(), 0)
            model_name_index = index.model().mapToSource(model_name_proxy_index)
            model_name = model_name_index.data()
            ref_file = mc.referenceQuery(model_name, f=1)
            obj = pipeFile.PathDetails.parse_path(ref_file)
            if obj.is_shd_file():
                shd_version = obj.shd_version
                editor.setCurrentIndex(editor.findText(shd_version))
        try:
            self.setModelData(editor, index.model(), index)
        except:pass
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, Qt.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def onCurrentIndexChanged(self, index):
        self.commitData.emit(self.sender())


class SwitchShader(QDialog):
    def __init__(self, parent=None):
        super(SwitchShader, self).__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle("Switch Shader")
        self.resize(400, 350)
        self.current_project = get_current_project.get_current_project()
        self.__db = sql_api.SqlApi(self.current_project)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)

        self.filter_layout = QHBoxLayout()
        self.filter_le = Filter()
        self.filter_layout.addStretch()
        self.filter_layout.addWidget(self.filter_le)
        self.update_btn = QToolButton()
        icon_path = join_path.join_path2(pipeGlobal.icons_dir, "update.png")
        self.update_btn.setIcon(QIcon(icon_path))
        self.update_btn.setStyleSheet("QToolButton{background:transparent;}"
                                      "QToolButton::hover{background:#00BFFF;border-color:#00BFFF;}")
        self.filter_layout.addWidget(self.update_btn)

        self.table_view = QTableView()
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setSortingEnabled(True)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.btn_layout = QHBoxLayout()
        self.switch_btn = QPushButton("Switch")
        self.cancel_btn = QPushButton("Cancel")
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.switch_btn)
        self.btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(self.filter_layout)
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(self.btn_layout)

        self.set_model()
        self.set_signals()

    def set_model(self):
        model_data = list()
        assets = get_asset_names.get_asset_names()
        if not assets:
            return
        assets = [asset.name() for asset in assets if pm.referenceQuery(asset, inr=1)]
        # {'assetName':'goushi','assetType':'asset','assetChildType':'character'}
        for asset in assets:
            asset_child_type, asset_name, temp = asset.split(":")[-1].split("_")
            arg_dict = {'assetName': asset_name, 'assetType': 'asset', 'assetChildType': ASSET_DICT[asset_child_type]}
            shd_version = self.__db.getShadeVersion(arg_dict)
            model_data.append([asset, shd_version])
        self.model = AssetTableModel(model_data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(0)
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setSourceModel(self.model)
        self.filter_le.textChanged.connect(self.set_filter)
        self.table_view.setModel(self.proxy_model)
        # delegate
        self.set_item_delegate()
        self.table_view.resizeColumnToContents(0)

    def set_item_delegate(self):
        image_delegate = ComboDelegate(self)
        self.table_view.setItemDelegateForColumn(1, image_delegate)
        self.show_item_delegate()

    def show_item_delegate(self):
        for i in xrange(self.proxy_model.rowCount()):
            self.table_view.openPersistentEditor(self.proxy_model.index(i, 1))

    def set_filter(self, value):
        self.proxy_model.setFilterRegExp(value)
        self.show_item_delegate()

    def set_signals(self):
        selection = self.table_view.selectionModel()
        if selection:
            selection.selectionChanged.connect(self.select_model)
        self.table_view.clicked.connect(self.select_model)
        self.update_btn.clicked.connect(self.set_model)
        self.switch_btn.clicked.connect(self.do_switch)
        self.cancel_btn.clicked.connect(self.close)

    def get_selected_assets(self):
        selected_indexes = self.table_view.selectedIndexes()
        if not selected_indexes:
            return
        selected_rows = list(set([self.proxy_model.mapToSource(i).row() for i in selected_indexes]))
        selected_assets = list()
        for row in selected_rows:
            asset_full_name = self.model.index(row, 0).data()
            shader_version = self.model.index(row, 1).data()
            shader_version = shader_version if isinstance(shader_version, basestring) else "default"
            selected_assets.append([asset_full_name, shader_version])
        return selected_assets

    def select_model(self):
        pm.select(clear=1)
        selected_assets = self.get_selected_assets()
        if not selected_assets:
            return
        for asset in selected_assets:
            mc.select(asset[0], add=1)

    def do_switch(self):
        selected_assets = self.get_selected_assets()
        if not selected_assets:
            return
        for asset in selected_assets:
            model_name = asset[0]
            asset_type_short_name = model_name.split(":")[-1].split("_")[0]
            asset_type = ASSET_DICT[asset_type_short_name]
            asset_name = model_name.split(":")[-1].split("_")[1]
            shd_version = asset[1]
            shd_file = pipeFile.get_asset_step_publish_file(asset_type, asset_name, "shd", self.current_project, shd_version)
            if shd_file:
                if os.path.isfile(shd_file):
                    ref_node = mc.referenceQuery(model_name, rfn=1)
                    ref_file = mc.referenceQuery(model_name, f=1)
                    if shd_file != ref_file:
                        replace_reference.replace_reference(ref_node, shd_file)
                        lgt_assign_shader_deformed.lgt_assign_shader_deformed(ref_node)
                else:
                    self.logger.error("%s %s %s shader file not exist." % (asset_type, asset_name, shd_version))
        self.message_box("Switch shader done.")

    @staticmethod
    def message_box(message):
        QMessageBox.information(None, "Warming Tip", message)


def main():
    ass = SwitchShader(get_maya_win.get_maya_win("PySide"))
    ass.show()
