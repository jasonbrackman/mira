# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from my_task_model import ListModel
from my_task_model import FilterProxyModel
from my_task_delegate import TaskCellWidget
from miraFramework.Filter import Filter
from miraFramework.refresh_btn import RefreshButton
from miraLibs.dbLibs import db_api
from miraFramework.combo import ProjectCombo
from miraLibs.pipeLibs import pipeFile


class TaskItem(object):
    def __init__(self, project, entity_type, asset_type_sequence, asset_name_shot, step, task,
                 status, status_color, start_date, due_date, pix_map):
        self.project = project
        self.entity_type = entity_type
        self.asset_type_sequence = asset_type_sequence
        self.asset_name_shot = asset_name_shot
        self.step = step
        self.task = task
        self.status = status
        self.status_color = status_color
        self.start_date = start_date
        self.due_date = due_date
        self.pix_map = pix_map


class TaskDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(TaskDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        cell_widget = TaskCellWidget(parent)
        return cell_widget

    def setEditorData(self, editor, index):
        item = index.model().data(index, Qt.DisplayRole)
        if item:
            editor.set_picture(item.pix_map)
            editor.set_entity(item.asset_type_sequence, item.asset_name_shot)
            editor.set_step_task(item.step, item.task)
            editor.set_status(item.status, item.status_color)
            editor.set_date(item.start_date, item.due_date)

    def sizeHint(self, option, index):
        return QSize(300, 100)


class MyTaskForm(QWidget):
    def __init__(self, parent=None):
        super(MyTaskForm, self).__init__(parent)
        self.setup_ui()
        self.db = db_api.DbApi(self.project).db_obj
        self.do_refresh()
        self.set_signals()

    def setup_ui(self):
        self.resize(380, 600)
        main_layout = QVBoxLayout(self)

        project_layout = QHBoxLayout()
        project_label = QLabel("Project")
        project_label.setFixedWidth(50)
        self.project_cbox = ProjectCombo()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        self.filter_le = Filter()

        layout = QHBoxLayout()
        self.final_check = QCheckBox("Delivered")
        self.refresh_btn = RefreshButton()
        layout.addWidget(self.final_check)
        layout.addStretch()
        layout.addWidget(self.refresh_btn)

        self.task_view = QListView()

        main_layout.addLayout(project_layout)
        main_layout.addWidget(self.filter_le)
        main_layout.addLayout(layout)
        main_layout.addWidget(self.task_view)

    def set_signals(self):
        self.refresh_btn.clicked.connect(self.do_refresh)
        self.final_check.stateChanged.connect(self.filter_finish)
        self.project_cbox.currentIndexChanged.connect(self.do_refresh)

    @property
    def project(self):
        return self.project_cbox.currentText()

    def get_my_tasks(self, unfinished):
        my_tasks = self.db.get_my_tasks(un_finished=unfinished)
        return my_tasks

    def set_model(self, my_tasks):
        model_data = list()
        for task in my_tasks:
            entity_type = self.db.get_task_entity_type(task)
            task_entity_id = task.get("item_id")
            task_entity_name = task.get("item").get("item_name")
            task_name = task.get("name")
            step = task.get("step").get("name")
            status = task.get("status").get("name")
            status_color = task.get("status").get("color")
            start_date = task.get("sub_date")
            due_date = task.get("due_date")
            priority = task.get("priority")
            if entity_type == "Asset":
                asset_type_sequence = self.db.get_asset_type_by_asset_id(task_entity_id)
            else:
                asset_type_sequence = self.db.get_sequence_by_shot_id(task_entity_id)
            image_path = pipeFile.get_task_workImage_file(self.project, entity_type, asset_type_sequence,
                                                          task_entity_name, step, task_name)
            if not os.path.isfile(image_path):
                image_path = os.path.abspath(os.path.join(__file__, "..", "unknown.png")).replace("\\", "/")
            pix_map = QPixmap(image_path)
            scaled = pix_map.scaled(130, 100, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            task_item = TaskItem(self.project, entity_type, asset_type_sequence, task_entity_name, step, task_name,
                                 status, status_color, start_date, due_date, scaled)
            model_data.append(task_item)
        if model_data:
            model = ListModel(model_data)
        else:
            model = QStandardItemModel()
        self.proxy_model = FilterProxyModel(self)
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setSourceModel(model)
        self.filter_le.textChanged.connect(self.set_filter)
        self.task_view.setModel(self.proxy_model)

    def init_model(self):
        my_tasks = self.get_my_tasks(True)
        self.set_model(my_tasks)

    def set_filter(self, value):
        self.proxy_model.set_name_filter(value)
        self.show_delegate()

    def set_delegate(self):
        delegate = TaskDelegate(self)
        self.task_view.setItemDelegate(delegate)
        self.show_delegate()

    def show_delegate(self):
        for i in xrange(self.proxy_model.rowCount()):
            self.task_view.openPersistentEditor(self.proxy_model.index(i, 0))

    def close_delegate(self):
        for i in xrange(self.proxy_model.rowCount()):
            self.task_view.closePersistentEditor(self.proxy_model.index(i, 0))

    def do_refresh(self):
        self.final_check.setChecked(False)
        self.init_model()
        self.close_delegate()
        self.set_delegate()

    def filter_finish(self, state):
        my_tasks = self.get_my_tasks(not state)
        self.set_model(my_tasks)
        self.close_delegate()
        self.set_delegate()


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(MyTaskForm)


if __name__ == "__main__":
    main()


