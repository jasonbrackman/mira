import os
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
import entity_ui
reload(entity_ui)
import task_ui
reload(task_ui)
from miraLibs.pipeLibs import pipeFile, Step
import miraCore


class TaskItem(object):
    def __init__(self, project, entity_type, asset_type_sequence, asset_name_shot, step, task, pix_map, actions,
                 status_name, status_color):
        self.project = project
        self.entity_type = entity_type
        self.asset_type_sequence = asset_type_sequence
        self.asset_name_shot = asset_name_shot
        self.step = step
        self.task = task
        self.pix_map = pix_map
        self.actions = actions
        self.status_name = status_name
        self.status_color = status_color


class Loader(QDialog):
    def __init__(self, parent=None):
        super(Loader, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.resize(800, 700)
        self.setWindowTitle("Loader")
        self.setup_ui()
        self.set_signals()
        self.__db = self.entity_ui.db
        self.__actions = self.entity_ui.get_actions()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_splitter = QSplitter(Qt.Horizontal)
        self.entity_ui = entity_ui.Entity()
        self.task_ui = task_ui.Task()

        main_splitter.addWidget(self.entity_ui)
        main_splitter.addWidget(self.task_ui)

        main_splitter.setSizes([self.width()*0.5, self.width()*0.5])
        main_splitter.setStretchFactor(1, 1)

        main_layout.addWidget(main_splitter)

    @property
    def project(self):
        return self.entity_ui.project_cbox.currentText()

    def set_signals(self):
        self.entity_ui.list_view.left_pressed.connect(self.show_tasks)

    def show_tasks(self, index):
        asset_name_shot = index.data(Qt.ToolTipRole)
        entity_type = self.entity_ui.entity_type
        asset_type_sequence = self.entity_ui.asset_type_sequence
        steps = self.__db.get_step(entity_type, asset_type_sequence, asset_name_shot)
        steps = list(set(steps))
        if "Art" in steps:
            steps.remove("Art")
        steps.sort()
        if not steps:
            self.task_ui.close_delegate()
            self.task_ui.set_model([])
            return
        model_data = list()
        ui_text = "<font face=Arial size=4 color=#00b4ff><b>%s  -  %s  -  %s</b></font>" \
                  % (entity_type, asset_type_sequence, asset_name_shot)
        for step in steps:
            engine = Step(self.project, step).engine
            tasks = self.__db.get_task(entity_type, asset_type_sequence, asset_name_shot, step)
            if not tasks:
                continue
            for task in tasks:
                task_name = task.get("code")
                status_name = task.get("status").get("name")
                status_color = task.get("status").get("color")
                if entity_type == "Asset":
                    format_str = "%s_asset_image" % engine
                else:
                    format_str = "%s_shot_image" % engine
                image_path = pipeFile.get_task_file(self.project, asset_type_sequence, asset_name_shot, step,
                                                    task_name, format_str, "", engine)
                if not os.path.isfile(image_path):
                    image_path = "%s/%s" % (miraCore.get_icons_dir(), "unknown.png")
                pix_map = QPixmap(image_path)
                pix_map = pix_map.scaled(100, 75, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                actions = self.__actions.get(entity_type)
                task_actions = actions.get("task").get("actions")
                item = TaskItem(self.project, entity_type, asset_type_sequence, asset_name_shot, step,
                                task_name, pix_map, task_actions, status_name, status_color)
                model_data.append(item)
        self.task_ui.set_label(ui_text)
        self.task_ui.set_model(model_data)
        self.task_ui.set_delegate()


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(Loader)
