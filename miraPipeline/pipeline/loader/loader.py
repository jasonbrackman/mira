# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import loader_ui
reload(loader_ui)
import miraCore
from miraLibs.pipeLibs import pipeMira, get_current_project
from miraLibs.dbLibs import db_api
from miraLibs.qtLibs import create_round_rect_thumbnail
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import join_path, yml_operation, start_file
from miraLibs.mayaLibs import maya_import, create_reference
from miraLibs.mayaLibs.Assembly import Assembly


IMAGE_WIDTH = 100


class AssetItem(object):
    def __init__(self, project=None, name=None, image=None):
        self.project = project
        self.name = name
        self.image = image


class LoaderModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(LoaderModel, self).__init__(parent)
        self.model_data = model_data

    def rowCount(self, parent=QModelIndex()):
        return len(self.model_data)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        item = self.model_data[row]
        if role == Qt.DisplayRole:
            name = item.name
            elidfont = QFontMetrics(QFont("Arial", 12))
            text = elidfont.elidedText(name, Qt.ElideRight, IMAGE_WIDTH)
            return text
        if role == Qt.ToolTipRole:
            return item.name
        if role == Qt.DecorationRole:
            image = item.image
            return image

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRows(self, position, count, value, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for index, i in enumerate(value):
            self.model_data.insert(position+index, i)
        self.model_data.sort(key=lambda x: x.name)
        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position+count-1)
        for i in range(count):
            value = self.model_data[position]
            self.model_data.remove(value)
        self.endRemoveRows()
        return True

    def setData(self, index, value, role):
        row = index.row()
        if value:
            if role == Qt.DecorationRole:
                self.model_data[row] = value
                self.dataChanged.emit(index, index)
            return True

    def remove_all(self):
        for i in xrange(self.rowCount()):
            self.removeRows(0, 1)


class Loader(loader_ui.LoaderUI):
    triggered = Signal()

    def __init__(self, parent=None):
        super(Loader, self).__init__(parent)
        self.init_project()
        self.init_asset_type()
        self.__db = db_api.DbApi(self.project).db_obj
        self.__image_dir = miraCore.get_icons_dir()
        self.main_menu = QMenu()
        self.entity_action_group = QActionGroup(self)
        self.task_action_group = QActionGroup(self)
        self.set_signals()

    @property
    def project(self):
        return self.project_cbox.currentText()

    @property
    def asset_type_sequence(self):
        if self.entity_type == "Asset":
            return self.asset_btn_grp.checkedButton().text()

    @property
    def entity_type(self):
        tab_index = self.entity_tab.currentIndex()
        if tab_index == 0:
            return "Asset"
        else:
            return "Shot"

    @property
    def pipeline_steps(self):
        if self.entity_type == "Asset":
            return pipeMira.get_studio_value(self.project, "asset_steps")
        else:
            return pipeMira.get_studio_value(self.project, "shot_steps")

    def init_project(self):
        projects = pipeMira.get_projects()
        current_project = get_current_project.get_current_project()
        self.project_cbox.addItems(projects)
        self.project_cbox.setCurrentIndex(self.project_cbox.findText(current_project))

    def init_asset_type(self):
        asset_types = pipeMira.get_studio_value(self.project, "asset_type")
        for asset_type in asset_types:
            self.asset_type_check = QCheckBox(asset_type)
            self.asset_btn_grp.addButton(self.asset_type_check)
            self.asset_layout.addWidget(self.asset_type_check)

    def set_signals(self):
        self.asset_btn_grp.buttonClicked[QAbstractButton].connect(self.show_assets)
        self.task_action_group.triggered.connect(self.on_task_action_triggered)
        self.entity_action_group.triggered.connect(self.on_entity_action_triggered)
        self.list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_context_menu)

    def set_model(self, model_data):
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter_le.textChanged.connect(self.proxy_model.setFilterRegExp)
        self.model = LoaderModel(model_data)
        self.proxy_model.setSourceModel(self.model)
        self.list_view.setModel(self.proxy_model)

    def show_assets(self, btn):
        project = self.project
        assets = self.__db.get_all_assets(self.asset_type_sequence)
        if not assets:
            return
        model_data = list()
        studio_conf_path = join_path.join_path2(miraCore.get_conf_dir(), "studio.yml")
        yml_data = yml_operation.get_yaml_data(studio_conf_path)
        project_data = yml_data.get(self.project)
        primary = project_data.get("primary")
        format_str = project_data.get("maya_asset_image")
        for asset in assets:
            asset_name = asset.get("name")
            image_path = format_str.format(primary=primary, project=project, asset_type=self.asset_type_sequence,
                                           asset_name=asset_name, step="MidMdl", task="MidMdl", engine="maya")
            if not os.path.isfile(image_path):
                image_path = join_path.join_path2(self.__image_dir, "unknown.png")
            image = create_round_rect_thumbnail.create_round_rect_thumbnail(image_path, IMAGE_WIDTH, IMAGE_WIDTH, 10)
            item = AssetItem(project, asset_name, image)
            model_data.append(item)
        self.set_model(model_data)

    def get_selected(self):
        selected_indexes = self.list_view.selectedIndexes()
        if not selected_indexes:
            return
        selected_rows = [self.proxy_model.mapToSource(index).row() for index in selected_indexes]
        selected_rows = list(set(selected_rows))
        selected = [self.model.model_data[row] for row in selected_rows]
        return selected

    def show_context_menu(self, pos):
        # add entity menu and action
        self.main_menu.clear()
        selected = self.get_selected()
        if not selected:
            return
        asset_shot_names = [item.name for item in selected]
        out_arg = [self.entity_type, self.asset_type_sequence, asset_shot_names]
        if self.entity_type == "Asset":
            ad_action = self.entity_action_group.addAction("AD")
            ad_action.attr = out_arg
            self.main_menu.addAction(ad_action)
        # add task menu and action
        if selected and len(selected) == 1:
            launch_action = self.entity_action_group.addAction("Launch Folder")
            launch_action.attr = out_arg
            self.main_menu.addAction(launch_action)
            asset_shot_name = asset_shot_names[0]
            out_arg = [self.entity_type, self.asset_type_sequence, asset_shot_name]
            steps = self.__db.get_step(self.entity_type, self.asset_type_sequence, asset_shot_name)
            if not steps:
                return
            steps = list(set(steps))
            steps.sort()
            for step in steps:
                step_menu = self.main_menu.addMenu(step)
                step_menu.up_level = self.main_menu
                tasks = self.__db.get_task(self.entity_type, self.asset_type_sequence, asset_shot_name, step)
                if not tasks:
                    continue
                for task in tasks:
                    task_name = task.get("name")
                    task_menu = step_menu.addMenu(task_name)
                    task_menu.up_level = step_menu
                    import_action = self.task_action_group.addAction("Import")
                    import_action.up_level = task_menu
                    import_action.attr = out_arg
                    reference_action = self.task_action_group.addAction("Reference")
                    reference_action.up_level = task_menu
                    reference_action.attr = out_arg
                    task_menu.addAction(import_action)
                    task_menu.addAction(reference_action)
        global_pos = self.list_view.mapToGlobal(pos)
        self.main_menu.exec_(global_pos)

    def get_publish_path(self, entity_type, typ, name, step, task):
        publish_file_path = None
        if entity_type == "Asset":
            publish_file_path = pipeFile.get_asset_task_publish_file(self.project, typ, name, step, task)
        return publish_file_path

    def on_task_action_triggered(self, action):
        task = action.up_level.title()
        step = action.up_level.up_level.title()
        entity_type, typ, name = action.attr
        publish_file_path = self.get_publish_path(entity_type, typ, name, step, task)
        if not os.path.isfile(publish_file_path):
            QMessageBox.warning(self, "Warming Tip", "%s is not an exist file." % publish_file_path)
            return
        if action.text() == "Import":
            maya_import.maya_import(publish_file_path)
        elif action.text() == "Reference":
            create_reference.create_reference(publish_file_path, name)
        else:
            return

    def on_entity_action_triggered(self, action):
        entity_type, typ, names = action.attr
        error_list = list()
        if action.text() == "AD":
            for name in names:
                ad_file_path = pipeFile.get_asset_AD_file(self.project, typ, name)
                if not os.path.isfile(ad_file_path):
                    error_list.append(ad_file_path)
                    continue
                assemb = Assembly()
                assemb.reference_ad("%s_AR" % name, ad_file_path)
            if error_list:
                QMessageBox.warning(self, "Warming Tip", "%s \n\nis not an exist file." % "\n\n".join(error_list))
        else:
            entity_dir = pipeFile.get_entity_dir(self.project, entity_type, "publish", typ, names[0])
            start_file.start_file(entity_dir)


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(Loader)


if __name__ == "__main__":
    main()
