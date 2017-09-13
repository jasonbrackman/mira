# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
import ui
from get_icon import get_icon
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import replace_reference
from miraLibs.log import Log


OBJECTNAME = "Replace Rig Reference"


class Asset(object):
    def __init__(self, name, thumbnail, is_rig, ref_file):
        self.name = name
        self.thumbnail = thumbnail
        self.is_rig = is_rig
        self.ref_file = ref_file


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
        context = pipeFile.PathDetails.parse_path(ref_file)
        is_rig = True if context.step == "HighRig" else False
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
                return self.arg[row].ref_file
        elif role == Qt.DecorationRole:
            if column == 2:
                return self.arg[row].thumbnail
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
        header_data = ["is_rig", "Assets", "Thumbnail", "file path", ""]
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
        self.switch_btn.clicked.connect(self.do_replace)
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
            pix_map = QPixmap(image_path)
            thumbnail = pix_map.scaled(QSize(100, 90), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            is_rig = self.maya.is_rig(ref_file)
            asset = Asset(grp, thumbnail, is_rig, ref_file)
            model_data.append(asset)
        return model_data

    @staticmethod
    def get_path(ref_file, get_type="image"):
        context = pipeFile.PathDetails.parse_path(ref_file)
        if not context:
            return
        project_name = context.project
        entity_type = context.entity_type
        asset_type = context.asset_type
        asset_name = context.asset_name
        current_step = context.step
        if current_step == "HighRig":
            step = "MidRig"
            task = "MidRig" if context.task == "HighRig" else context.task
        else:
            step = "HighRig"
            task = "HighRig" if context.task == "MidRig" else context.task
        if get_type == "image":
            path = pipeFile.get_task_file(project_name, asset_type, asset_name, step, task,
                                          "maya_asset_image", version="")
        else:
            path = pipeFile.get_task_publish_file(project_name, entity_type, asset_type, asset_name, step, task)
        return path

    def get_image_path(self, ref_file):
        return self.get_path(ref_file)

    def get_rig_publish_path(self, ref_file):
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

    def do_replace(self):
        selected = self.get_selected()
        if not selected:
            return
        for asset_item in selected:
            group_name = asset_item.name
            ref_file = self.maya.get_reference_file(group_name)
            rig_path = self.get_rig_publish_path(ref_file)
            if not rig_path:
                Log.warning("%s is not an exist file" % rig_path)
                continue
            ref_node = self.maya.get_reference_node(group_name)
            replace_reference.replace_reference(ref_node, rig_path)
        self.do_update()


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(ReplaceRigReference)
