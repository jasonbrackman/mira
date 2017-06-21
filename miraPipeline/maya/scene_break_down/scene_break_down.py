# -*- coding: utf-8 -*-
import os
import logging
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import pymel.core as pm
from miraLibs.pyLibs import get_latest_version
from miraLibs.mayaLibs import get_maya_win
from miraLibs.pipeLibs.pipeMaya import lgt_assign_shader_deformed


class ReferenceImageDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ReferenceImageDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == 0:
            label = QLabel(parent)
            return label

    def setEditorData(self, editor, index):
        model = index.model()
        data_index = model.index(index.row(), 4)
        value = model.data(data_index, Qt.DisplayRole).icon_path
        if value:
            pix_map = QPixmap(value)
            editor.setPixmap(pix_map)


class ReferenceTableModel(QAbstractTableModel):
    def __init__(self, arg=[], parent=None):
        super(ReferenceTableModel, self).__init__(parent)
        self.arg = arg

    def rowCount(self, parent):
        return len(self.arg)

    def columnCount(self, parent):
        return len(self.arg[0])

    def data(self, index, role):
        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            if column == 0:
                return None
            return self.arg[row][column]
        if role == Qt.ToolTipRole:
            if column == 1:
                ref_node = pm.PyNode(self.arg[row][column])
                file_name = ref_node.referenceFile().path
                return file_name

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if value:
                self.arg[row][column] = value
                self.dataChanged.emit(index, index)
            return True
        return False


class ReferenceItem(object):
    def __init__(self):
        self.icon_path = None
        self.path = None
        self.text = None
        self.type = None


class SceneBreakDown(QDialog):
    close_signal = Signal()

    def __init__(self, parent=None):
        super(SceneBreakDown, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle("Scene Break Down")
        self.resize(550, 650)
        self.icon_dir = os.path.join(os.path.dirname(__file__), "icons")
        self.green_icon_path = os.path.join(self.icon_dir, "green_bullet.png")
        self.red_icon_path = os.path.join(self.icon_dir, "red_bullet.png")
        # UI
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 2)
        # proxy filter
        proxy_filter_layout = QHBoxLayout()
        self.proxy_filter_le = QLineEdit()
        proxy_filter_layout.addStretch()
        proxy_filter_layout.addWidget(self.proxy_filter_le)
        # -reference view
        self.reference_view = QTableView()
        self.reference_view.horizontalHeader().setStretchLastSection(True)
        self.reference_view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.reference_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.reference_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.reference_view.verticalHeader().hide()
        self.reference_view.horizontalHeader().hide()
        self.show_in_file_system_action = QAction("Show in File System", self)
        self.reference_view.addAction(self.show_in_file_system_action)
        self.model = None
        self.proxy_model = None
        self.set_model()
        # -bottom layout
        bottom_layout = QHBoxLayout()
        # --filter layout
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_group = QGroupBox()
        filter_layout.addWidget(filter_group)
        check_layout = QHBoxLayout(filter_group)
        check_layout.setContentsMargins(3, 1, 0, 1)
        filter_label = QLabel("Filters")
        self.check_btn_group = QButtonGroup()
        self.check_btn_group.setExclusive(False)
        self.green_check = QCheckBox()
        self.green_check.setChecked(True)
        self.green_check.setIcon(QIcon(self.green_icon_path))
        self.red_check = QCheckBox()
        self.red_check.setChecked(True)
        self.red_check.setIcon(QIcon(self.red_icon_path))
        check_layout.addWidget(filter_label)
        check_layout.addWidget(self.green_check)
        check_layout.addWidget(self.red_check)
        self.check_btn_group.addButton(self.green_check)
        self.check_btn_group.addButton(self.red_check)
        # --button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(2)
        self.refresh_btn = QPushButton("Refresh")
        self.update_all_red_btn = QPushButton("Update All Red")
        self.update_selected_btn = QPushButton("Update Selected")
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.update_all_red_btn)
        button_layout.addWidget(self.update_selected_btn)
        bottom_layout.addLayout(filter_layout)
        bottom_layout.addStretch()
        bottom_layout.addLayout(button_layout)
        main_layout.addLayout(proxy_filter_layout)
        main_layout.addWidget(self.reference_view)
        main_layout.addLayout(bottom_layout)
        self.set_signals()
        
    def set_signals(self):
        self.check_btn_group.buttonClicked.connect(self.do_filter)
        self.refresh_btn.clicked.connect(self.refresh_model)
        self.show_in_file_system_action.triggered.connect(self.show_in_file_system)
        self.update_all_red_btn.clicked.connect(self.update_all_red)
        self.update_selected_btn.clicked.connect(self.update_selected)
        self.proxy_filter_le.textChanged.connect(self.proxy_model.setFilterRegExp)
        self.proxy_filter_le.textChanged.connect(self.set_delegate)

    def set_model(self):
        model_data = self.get_model_data()
        self.proxy_model = QSortFilterProxyModel()
        if not model_data:
            return
        self.model = ReferenceTableModel(model_data)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(1)
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.reference_view.setModel(self.proxy_model)
        self.reference_view.setSortingEnabled(True)
        # delegates
        self.set_delegate()
        # set column width
        column_width_list = [20, 100, self.width()-46]
        for column in range(3):
            self.reference_view.setColumnWidth(column, column_width_list[column])
        self.reference_view.resizeColumnToContents(1)
        self.reference_view.hideColumn(3)
        self.reference_view.hideColumn(4)

    def set_delegate(self):
        image_delegate = ReferenceImageDelegate(self.reference_view)
        self.reference_view.setItemDelegateForColumn(0, image_delegate)
        for i in xrange(self.proxy_model.rowCount()):
            self.reference_view.openPersistentEditor(self.proxy_model.index(i, 0))

    def get_model_data(self):
        reference_model_data = self.get_reference_model_data()
        exocortex_model_data = self.get_exocortex_model_data()
        model_data = reference_model_data + exocortex_model_data
        return model_data

    def get_reference_model_data(self):
        model_data = list()
        references = pm.ls(type="reference")
        if references:
            for ref in references:
                if ref.name() in ["sharedReferenceNode"]:
                    continue
                item = ReferenceItem()
                item.type = "reference"
                ref_path = pm.referenceQuery(ref, filename=1, wcn=1)
                item.path = ref_path
                latest_path_list = get_latest_version.get_latest_version(ref_path)
                if not latest_path_list:
                    continue
                latest_path = latest_path_list[0]
                latest_path = latest_path.replace("\\", "/")
                if not ref_path == latest_path:
                    item.icon_path = self.red_icon_path
                else:
                    item.icon_path = self.green_icon_path
                item.text = ref.name()
                model_data.append([item.icon_path, item.text, item.path, item.type, item])
        return model_data

    def get_exocortex_model_data(self):
        model_data = list()
        exocortex_nodes = pm.ls(type="ExocortexAlembicFile")
        if exocortex_nodes:
            for node in exocortex_nodes:
                item = ReferenceItem()
                file_name = node.fileName.get()
                latest_path = get_latest_version.get_latest_version(file_name)[0]
                latest_path = latest_path.replace("\\", "/")
                if not file_name == latest_path:
                    item.icon_path = self.red_icon_path
                else:
                    item.icon_path = self.green_icon_path
                item.text = node.name()
                item.path = file_name
                item.type = "exocortex"
                model_data.append([item.icon_path, item.text, item.path, item.type, item])
        return model_data

    def do_filter(self):
        status_list = []
        if self.green_check.isChecked():
            status_list.append(self.green_icon_path)
        if self.red_check.isChecked():
            status_list.append(self.red_icon_path)
        self.filter(status_list)

    def filter(self, status_list):
        for i in xrange(self.model.rowCount(self)):
            model_index = self.model.index(i, 4)
            item = self.model.data(model_index, Qt.DisplayRole)
            if not status_list:
                self.reference_view.hideRow(i)
            else:
                self.reference_view.showRow(i)
                if item.icon_path not in status_list:
                    self.reference_view.hideRow(i)
                else:
                    self.reference_view.showRow(i)

    def refresh_model(self):
        self.proxy_filter_le.setText("")
        self.green_check.setChecked(True)
        self.red_check.setChecked(True)
        self.set_model()
        self.set_signals()

    @staticmethod
    def update_reference(ref_node):
        path = ref_node.referenceFile().path
        latest_version = get_latest_version.get_latest_version(path)[0].replace("\\", "/")
        if path != latest_version:
            if os.path.isfile(latest_version):
                rn = pm.system.FileReference(ref_node)
                rn.replaceWith(latest_version)
            else:
                logging.warning("%s is not an exist file." % latest_version)
        # assign shader to deformed.
        lgt_assign_shader_deformed.lgt_assign_shader_deformed(ref_node.name())

    @staticmethod
    def update_exocortex(exocortex_node):
        path = exocortex_node.fileName.get()
        latest_version = get_latest_version.get_latest_version(path)[0].replace("\\", "/")
        if path != latest_version:
            if os.path.isfile(latest_version):
                exocortex_node.fileName.set(latest_version)
            else:
                logging.warning("%s is not an exist file." % latest_version)

    def get_items(self, selected=True):
        items = list()
        if selected:
            selected_indexes = self.reference_view.selectedIndexes()
            if selected_indexes:
                rows = list(set([selected_index.row() for selected_index in selected_indexes]))
                for row in rows:
                    item_proxy_index = self.proxy_model.index(row, 4)
                    item = self.proxy_model.mapToSource(item_proxy_index).data()
                    items.append(item)
        else:
            for i in xrange(self.model.rowCount(self)):
                proxy_model_index = self.proxy_model.index(i, 4)
                model_index = self.proxy_model.mapToSource(proxy_model_index)
                item = model_index.data()
                items.append(item)
        return items

    def show_in_file_system(self):
        items = self.get_items()
        if not items:
            return
        for item in items:
            path = item.path
            dir_name = os.path.dirname(path)
            if os.path.isdir(dir_name):
                os.startfile(dir_name)
            else:
                logging.error("%s is not an exist directory" % dir_name)

    def do_update(self, selected=True):
        items = self.get_items(selected)
        if not items:
            return
        for item in items:
            if item.icon_path == self.red_icon_path:
                node = pm.PyNode(item.text)
                if item.type == "reference":
                    self.update_reference(node)
                else:
                    self.update_exocortex(node)
        self.refresh_model()

    def update_all_red(self):
        self.do_update(False)

    def update_selected(self):
        self.do_update(True)

    def closeEvent(self, *args, **kwargs):
        self.close_signal.emit()
        self.deleteLater()


def main():
    sbd = SceneBreakDown(get_maya_win.get_maya_win("PySide"))
    sbd.show()


if __name__ == "__main__":
    main()
