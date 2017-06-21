# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
import ui
from get_icon import get_icon
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_maya_win, replace_reference


OBJECTNAME = "Replace Rig Reference"


class Asset(object):
    def __init__(self, name, thumbnail, is_rig, rig_path):
        self.name = name
        self.thumbnail = thumbnail
        self.is_rig = is_rig
        self.rig_path = rig_path


class Maya(object):

    @staticmethod
    def is_reference(group):
        return mc.referenceQuery(group, isNodeReferenced=1)

    def get_rig_group(self):
        all_root_group = mc.ls("*:*_ROOT") + mc.ls("*_ROOT")
        reference_rig_grp = [group for group in all_root_group if self.is_reference(group)]
        return reference_rig_grp

    def get_reference_file(self, group):
        if not self.is_reference(group):
            return
        ref_file = mc.referenceQuery(group, filename=1, withoutCopyNumber=1)
        return ref_file

    @staticmethod
    def is_rig(ref_file):
        ref_file = ref_file.replace("\\", "/")
        is_rig = True if "/rig/" in ref_file else False
        return is_rig

    @staticmethod
    def clear_selection():
        mc.select(clear=1)

    @staticmethod
    def select(maya_object):
        mc.select(maya_object, r=1)

    @staticmethod
    def get_reference_node(group_name):
        return mc.referenceQuery(group_name, referenceNode=1)


class AssetTableModel(QAbstractTableModel):
    def __init__(self, arg=[], parent=None):
        super(AssetTableModel, self).__init__(parent)
        self.arg = arg

    def rowCount(self, parent):
        return len(self.arg)

    def columnCount(self, parent):
        return 4

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            if column == 1:
                return self.arg[row].name
            if column == 3:
                return self.arg[row].rig_path
        elif role == Qt.DecorationRole:
            if column == 2:
                pix_map = QPixmap(self.arg[row].thumbnail)
                scaled = pix_map.scaled(QSize(90, 90), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                return scaled
            if column == 0:
                is_rig = self.arg[row].is_rig
                if is_rig:
                    pix_map = QPixmap(get_icon(True))
                else:
                    pix_map = QPixmap(get_icon(False))
                return pix_map

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.arg[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
        header_data = ["is_rig", "Assets", "Thumbnail", "rig_path", ""]
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return header_data[section]


class ReplaceRigReference(ui.ReplaceUI):
    def __init__(self, parent=None):
        super(ReplaceRigReference, self).__init__(parent)
        self.setObjectName(OBJECTNAME)
        self.maya = Maya()
        self.set_model()
        self.set_signals()

    def set_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        selection = self.table_view.selectionModel()
        if selection:
            selection.selectionChanged.connect(self.select_model)
        self.table_view.clicked.connect(self.select_model)
        self.update_btn.clicked.connect(self.do_update)
        self.switch_btn.clicked.connect(self.replace_lowRig_to_rig)
        self.check_btn_group.buttonClicked.connect(self.do_filter)

    def do_update(self):
        self.set_model()
        self.set_table_view()
        self.green_check.setChecked(True)
        self.red_check.setChecked(True)
        for row in xrange(self.model.rowCount(QModelIndex)):
            self.table_view.showRow(row)

    def set_model(self):
        model_data = self.get_model_data()
        if not model_data:
            return
        self.model = AssetTableModel(model_data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(1)
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setSourceModel(self.model)
        self.filter_le.textChanged.connect(self.set_filter)
        self.table_view.setModel(self.proxy_model)
        self.set_table_view()

    def set_table_view(self):
        self.table_view.setFocusPolicy(Qt.NoFocus)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.resizeRowsToContents()
        self.table_view.resizeColumnToContents(1)
        self.table_view.resizeColumnToContents(3)

    def set_filter(self, value):
        self.proxy_model.setFilterRegExp(value)
        self.set_table_view()

    def do_filter(self):
        check_status = list()
        if self.green_check.isChecked():
            check_status.append(True)
        if self.red_check.isChecked():
            check_status.append(False)
        for row in xrange(self.model.rowCount(QModelIndex)):
            item = self.model.arg[row]
            is_rig = item.is_rig
            if is_rig not in check_status:
                self.table_view.hideRow(row)
            else:
                self.table_view.showRow(row)

    def get_model_data(self):
        model_data = list()
        group = self.maya.get_rig_group()
        if not group:
            return
        for grp in group:
            ref_file = self.maya.get_reference_file(grp)
            image_path = self.get_image_path(ref_file)
            is_rig = self.maya.is_rig(ref_file)
            rig_path = self.get_publish_path(ref_file)
            asset = Asset(grp, image_path, is_rig, rig_path)
            model_data.append(asset)
        return model_data

    @staticmethod
    def get_path(ref_file, get_type="image"):
        obj = pipeFile.PathDetails.parse_path(ref_file)
        if not obj:
            return
        asset_type = obj.asset_type
        asset_name = obj.asset_name
        category = obj.category
        project_name = obj.project
        rig_version = obj.context_version
        if get_type == "image":
            path = pipeFile.get_asset_step_image_file(asset_type, asset_name, category,
                                                      project_name, rig_version=rig_version)
        else:
            path = pipeFile.get_asset_step_publish_file(asset_type, asset_name, "rig",
                                                        project_name, rig_version=rig_version)
        return path

    def get_image_path(self, ref_file):
        return self.get_path(ref_file)

    def get_publish_path(self, ref_file):
        return self.get_path(ref_file, "publish")

    def get_selected(self):
        selected_indexes = self.table_view.selectedIndexes()
        if not selected_indexes:
            return
        selected_rows = list(set([self.proxy_model.mapToSource(i).row() for i in selected_indexes]))
        selected = [self.model.arg[row] for row in selected_rows]
        return selected

    def select_model(self):
        selected = self.get_selected()
        if not selected:
            return
        self.maya.clear_selection()
        selected_maya_obj = [asset_item.name for asset_item in selected]
        self.maya.select(selected_maya_obj)

    def replace_lowRig_to_rig(self):
        selected = self.get_selected()
        if not selected:
            return
        for asset_item in selected:
            group_name = asset_item.name
            rig_path = asset_item.rig_path
            if not rig_path:
                continue
            ref_node = self.maya.get_reference_node(group_name)
            replace_reference.replace_reference(ref_node, rig_path)
            asset_item.is_rig = True
        self.do_update()


def main():
    if mc.window(OBJECTNAME, q=1, ex=1):
        mc.deleteUI(OBJECTNAME)
    rrr = ReplaceRigReference(get_maya_win.get_maya_win("PySide"))
    rrr.show()
