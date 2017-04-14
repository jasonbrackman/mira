# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
import pymel.core as pm
import miraCore
from miraLibs.pipeLibs.pipeMaya import get_asset_names, assign_shader, get_current_project
from miraLibs.mayaLibs import get_maya_win
from miraFramework.Filter import ButtonLineEdit
from miraLibs.pyLibs import join_path
from miraLibs.pipeLibs.pipeDb import sql_api


class PopDialog(QtGui.QDialog):
    def __init__(self, data_list=[], parent=None):
        super(PopDialog, self).__init__(parent)
        # data_list --->first argument: asset_name; second argument: not exist model list
        self.data_list = data_list
        self.resize(600, 300)
        self.setWindowTitle("Assign shader information")
        main_layout = QtGui.QHBoxLayout(self)
        main_layout.setContentsMargins(1, 0, 1, 0)
        self.create_table()
        main_layout.addWidget(self.info_table)

    def create_table(self):
        self.info_table = QtGui.QTableWidget()
        self.info_table.verticalHeader().setVisible(False)
        self.info_table.setColumnCount(2)
        self.info_table.setRowCount(len(self.data_list))
        self.info_table.setHorizontalHeaderLabels(["Asset", "Not exist models"])
        self.info_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.info_table.horizontalHeader().setStretchLastSection(True)
        self.info_table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.set_table_data()
        self.info_table.resizeColumnToContents(0)

    def set_table_data(self):
        if not self.data_list:
            return
        for index, data in enumerate(self.data_list):
            asset_name = data[0]
            not_exist_model_list = data[1]
            asset_item = QtGui.QTableWidgetItem(asset_name)
            self.info_table.setItem(index, 0, asset_item)
            if not_exist_model_list:
                model_list_widget = QtGui.QListWidget()
                model_list_widget.addItems(not_exist_model_list)
                model_list_widget.itemDoubleClicked.connect(self.set_item_editable)
                self.info_table.setCellWidget(index, 1, model_list_widget)
                self.info_table.setRowHeight(index, 100)
            else:
                model_item = QtGui.QTableWidgetItem(u"√")
                model_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.info_table.setItem(index, 1, model_item)

    @staticmethod
    def set_item_editable(item):
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)


class AssetTableModel(QtCore.QAbstractTableModel):
    def __init__(self, arg=[], header=[], parent=None):
        super(AssetTableModel, self).__init__(parent)
        self.__arg = arg
        self.__header = header

    @property
    def arg(self):
        return self.__arg

    @arg.setter
    def arg(self, value):
        self.__arg = value

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, value):
        self.__header = value

    def rowCount(self, parent):
        return len(self.__arg)

    def columnCount(self, parent):
        return len(self.__arg[0])

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self.__arg[row][column]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            self.__arg[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__header[section]


class ComboDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        super(ComboDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == 1:
            combo = QtGui.QComboBox(parent)
            combo.currentIndexChanged.connect(self.onCurrentIndexChanged)
            return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        if isinstance(value, list):
            editor.addItems(value)
            editor.setCurrentIndex(editor.findText("default"))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def onCurrentIndexChanged(self, index):
        self.commitData.emit(self.sender())


class AssignShader(QtGui.QDialog):
    def __init__(self, parent=None):
        super(AssignShader, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowTitle("Assign Shader")
        self.resize(400, 350)
        current_project = get_current_project.get_current_project()
        self.__db = sql_api.SqlApi(current_project)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)

        self.filter_layout = QtGui.QHBoxLayout()
        self.filter_le = ButtonLineEdit()
        self.filter_layout.addStretch()
        self.filter_layout.addWidget(self.filter_le)
        self.update_btn = QtGui.QToolButton()
        icon_path = join_path.join_path2(miraCore.get_icons_dir(), "update.png")
        self.update_btn.setIcon(QtGui.QIcon(icon_path))
        self.update_btn.setStyleSheet("QToolButton{background:transparent;}"
                                      "QToolButton::hover{background:#00BFFF;border-color:#00BFFF;}")
        self.filter_layout.addWidget(self.update_btn)

        self.table_view = QtGui.QTableView()
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setSortingEnabled(True)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.btn_layout = QtGui.QHBoxLayout()
        self.assign_shader_btn = QtGui.QPushButton("Assign Shader")
        self.assign_lambert_btn = QtGui.QPushButton("Assign Lambert")
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.assign_shader_btn)
        self.btn_layout.addWidget(self.assign_lambert_btn)

        main_layout.addLayout(self.filter_layout)
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(self.btn_layout)

        self.set_model()
        self.set_signals()

    def set_model(self):
        headers = ["Assets", "Shader Version"]
        model_data = list()
        assets = get_asset_names.get_asset_names()
        if not assets:
            return
        assets = [asset.name() for asset in assets]
        # {'assetName':'goushi','assetType':'asset','assetChildType':'character'}
        asset_dict = {"char": "character", "prop": "prop", "env": "environment"}
        for asset in assets:
            asset_child_type, asset_name, temp = asset.split(":")[-1].split("_")
            arg_dict = {'assetName': asset_name, 'assetType': 'asset', 'assetChildType': asset_dict[asset_child_type]}
            shd_version = self.__db.getShadeVersion(arg_dict)
            model_data.append([asset, shd_version])
        self.model = AssetTableModel(model_data, headers)
        self.proxy_model = QtGui.QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(0)
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
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
        self.assign_shader_btn.clicked.connect(self.assign_shader)
        self.assign_lambert_btn.clicked.connect(self.assign_lambert)

    def get_selected_assets(self):
        selected_indexes = self.table_view.selectedIndexes()
        if not selected_indexes:
            return
        selected_rows = list(set([self.proxy_model.mapToSource(i).row() for i in selected_indexes]))
        selected_assets = list()
        for row in selected_rows:
            asset_full_name = pm.PyNode(self.model.index(row, 0).data())
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
            pm.select(asset[0], add=1)

    def assign_shader(self):
        selected_assets = self.get_selected_assets()
        data_list = list()
        for asset in selected_assets:
            not_exist_list = assign_shader.assign_shader(*asset)
            data_list.append([asset[0].name(), not_exist_list])
        pop_dialog = PopDialog(data_list, self)
        pop_dialog.show()

    def assign_lambert(self):
        selected_assets = self.get_selected_assets()
        if not selected_assets:
            return
        for asset in selected_assets:
            pm.sets("initialShadingGroup", fe=asset[0])
        self.message_box("Assign lambert done.")

    @staticmethod
    def message_box(message):
        QtGui.QMessageBox.information(None, "Warming Tip", message)


def main():
    ass = AssignShader(get_maya_win.get_maya_win("PySide"))
    ass.show()
