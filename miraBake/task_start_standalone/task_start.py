# -*- coding: utf-8 -*-
import getpass
import os
import subprocess
import sys
from PySide import QtGui, QtCore
import task_start_ui
import miraCore
from miraLibs.pipeLibs import pipeMira, pipeFile, get_logger, pipeHistory
from miraLibs.pyLibs import join_path, Path
from miraLibs.sgLibs import Sg
from miraLibs.pipeLibs.pipeMaya import get_current_project
from miraLibs.pipeLibs.pipeSg import create_filesystem_structure


class RunCommandThread(QtCore.QThread):

    def __init__(self, command=None, callback=None, file_name=None, logger=None, parent=None):
        super(RunCommandThread, self).__init__(parent)
        self.__command = command
        self.__callback = callback
        self.__file_name = file_name
        self.__logger = logger
        if self.__callback:
            self.finished.connect(self.run_callback)

    def run(self):
        p = subprocess.Popen(self.__command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            return_code = p.poll()
            if return_code == 0:
                break
            elif return_code == 1:
                raise Exception(self.__command + " was terminated for some reason.")
            elif return_code is not None:
                raise Exception(self.__command + " was crashed for some reason.")
            line = p.stdout.readline()
            if line.strip():
                self.__logger.info(line)

    def run_callback(self):
        if os.path.isfile(self.__file_name):
            self.__callback(True, self.__file_name)
        else:
            self.__callback(False, self.__file_name)
            self.__logger.error("Something wrong with run start file.")


class TaskManager(task_start_ui.TaskStartUI):

    def __init__(self, parent=None):
        super(TaskManager, self).__init__(parent)
        self.__threads = list()
        self.__logger = None
        self.__user = getpass.getuser()
        self.__project = get_current_project.get_current_project()
        self.__mayabatch = pipeMira.get_mayabatch_path(self.__project)
        self.__primary = pipeMira.get_primary_dir(self.__project)
        self.__sg = Sg.Sg(self.__project)
        self.__asset_types = pipeMira.get_asset_type()
        self.__asset_steps = pipeMira.get_asset_step()
        self.__shot_steps = pipeMira.get_shot_step()
        self.__scene_steps = pipeMira.get_scene_step()
        self.__engine = self.engine_btn_grp.checkedButton().text()
        self.set_style()
        self.init()
        self.set_signals()

    def set_style(self):
        qss_path = join_path.join_path2(os.path.dirname(__file__), "style.qss")
        self.setStyle(QtGui.QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())

    def init(self):
        self.init_project()
        self.init_priority()
        self.init_user()

    def init_project(self):
        projects = pipeMira.get_projects()
        self.project_cbox.addItems(projects)
        self.project_cbox.setCurrentIndex(self.project_cbox.findText(self.__project))
        self.path_le.setText(self.__primary)

    def init_priority(self):
        self.on_project_changed(self.__project)

    def init_user(self):
        users = self.__sg.get_users()
        user_names = [user["name"] for user in users]
        self.user_widget.set_model_data(user_names)

    def set_signals(self):
        self.project_cbox.currentIndexChanged[str].connect(self.on_project_changed)
        self.entity_btn_grp.buttonClicked.connect(self.init_grp)
        self.engine_btn_grp.buttonClicked.connect(self.set_engine)
        self.first_widget.list_view.clicked.connect(self.show_asset_or_shot)
        self.second_widget.list_view.clicked.connect(self.show_step)
        self.third_widget.list_view.clicked.connect(self.show_task)
        self.fourth_widget.list_view.clicked.connect(self.show_path)
        self.publish_task_btn.clicked.connect(self.do_publish)
        self.cancel_btn.clicked.connect(self.close)
        self.path_btn.clicked.connect(self.open_path)

    def on_project_changed(self, project):
        self.__project = project
        priority = pipeMira.get_site_value(project, "priority")
        self.priority_cbox.addItems(priority)
        self.__sg = Sg.Sg(self.__project)
        for widget in [self.first_widget, self.second_widget, self.third_widget, self.fourth_widget]:
            widget.list_view.clear()

    def init_grp(self):
        checked_btn_text = self.entity_btn_grp.checkedButton().text()
        for widget in [self.first_widget, self.second_widget, self.third_widget, self.fourth_widget]:
            widget.list_view.clear()
        if checked_btn_text == "Asset":
            # set group name
            self.first_widget.set_group_name("Asset Type")
            self.second_widget.set_group_name("Asset")
            self.second_widget.list_view.clear()
            # init list view
            self.first_widget.set_model_data(self.__asset_types)
        else:
            self.first_widget.set_group_name("Sequence")
            self.second_widget.set_group_name("Shot")
            self.second_widget.list_view.clear()
            # init list view
            sequences = self.__sg.get_sequence()
            self.first_widget.set_model_data(sequences)

    def set_engine(self):
        self.__engine = self.engine_btn_grp.checkedButton().text()
        self.show_path()

    def show_asset_or_shot(self, index):
        for widget in [self.second_widget, self.third_widget, self.fourth_widget]:
            widget.list_view.clear()
        selected = index.data()
        checked = self.entity_btn_grp.checkedButton().text()
        if checked == "Asset":
            assets = self.__sg.get_all_assets(selected)
            asset_names = [asset["code"] for asset in assets]
            self.second_widget.set_model_data(asset_names)
        elif checked == "Shot":
            shots = self.__sg.get_all_shots_by_sequence(selected)
            shot_names = [shot["name"] for shot in shots]
            self.second_widget.set_model_data(shot_names)

    def show_step(self, index):
        for widget in [self.third_widget, self.fourth_widget]:
            widget.list_view.clear()
        entity_type = self.entity_btn_grp.checkedButton().text()
        asset_or_shot = index.data()
        asset_type_or_sequence = self.first_widget.list_view.get_selected()
        if not asset_type_or_sequence:
            return
        steps = self.__sg.get_step(entity_type, asset_type_or_sequence, asset_or_shot)
        step_names = list(set(steps))
        self.third_widget.set_model_data(step_names)

    def show_task(self, index):
        self.fourth_widget.list_view.clear()
        entity_type = self.entity_btn_grp.checkedButton().text()
        asset_type_or_sequence = self.first_widget.list_view.get_selected()
        asset_or_shot = self.second_widget.list_view.get_selected()
        step = index.data()
        if not all((asset_type_or_sequence, asset_or_shot)):
            return
        tasks = self.__sg.get_task(entity_type, asset_type_or_sequence, asset_or_shot, step)
        if not tasks:
            return
        task_names = [task["content"] for task in tasks]
        self.fourth_widget.set_model_data(task_names)

    def show_path(self):
        entity_type = self.entity_btn_grp.checkedButton().text()
        first_selected = self.first_widget.list_view.get_selected()
        second_selected = self.second_widget.list_view.get_selected()
        third_selected = self.third_widget.list_view.get_selected()
        fourth_selected = self.fourth_widget.list_view.get_selected()
        if not all((first_selected, second_selected, third_selected, fourth_selected)):
            return
        if entity_type == "Asset":
            template = pipeMira.get_site_value(self.__project, "%s_asset_work" % self.__engine)
            file_path = template.format(primary=self.__primary, project=self.__project, asset_type=first_selected[0],
                                        asset_name=second_selected[0].split("_")[-1], step=third_selected[0],
                                        task=fourth_selected[0], version="000", engine=self.__engine)
        else:
            template = pipeMira.get_site_value(self.__project, "%s_shot_work" % self.__engine)
            file_path = template.format(primary=self.__primary, project=self.__project, sequence=first_selected[0],
                                        shot=second_selected[0].split("_")[-1], step=third_selected[0],
                                        task=fourth_selected[0], version="000", engine=self.__engine)
        self.path_le.setText(file_path)

    def open_path(self):
        path = self.path_le.text()
        if path:
            p = Path.Path(path)
            dir_name = Path.Path(p.dirname())
            dir_name.startfile()
            
    def create_origin_file(self, file_name):
        obj = pipeFile.PathDetails.parse_path(file_name)
        step = obj.step
        if step == "art":
            return
        scripts_dir = miraCore.get_scripts_dir()
        start_dir = join_path.join_path2(scripts_dir, "pipeTools", self.__engine, "start")
        start_file_name = "%s_start.py" % step
        start_file = join_path.join_path2(start_dir, start_file_name)
        if not os.path.isfile(start_file):
            QtGui.QMessageBox.warning(self, "Warning", "%s is not an exist file." % start_file)
            return
        cmd = "%s -command \"python \\\"file_name='%s';execfile('%s')\\\"\"" % (
            self.__mayabatch, file_name, start_file)
        cmd = str(cmd)
        self.__logger.info(cmd)
        thread = RunCommandThread(cmd, self.call_back, file_name, self.__logger)
        thread.start()
        self.__threads.append(thread)
        self.progress_bar.show()
        self.progress_bar.setRange(0, 0)
        
    def do_publish(self):
        origin_work_file = self.path_le.text()
        if not origin_work_file:
            return
        asset_or_shot = self.second_widget.list_view.get_selected()[0]
        step = self.third_widget.list_view.get_selected()[0]
        task = self.fourth_widget.list_view.get_selected()[0]
        logger_base_name = "%s_%s_%s" % (asset_or_shot, step, task)
        self.__logger = get_logger.get_logger(self.__project, "create", logger_base_name)
        if os.path.isfile(origin_work_file):
            message_info = "%s \n is an exist file,Do you want to overwrite it?" % origin_work_file
        else:
            message_info = "Do you want to publish this task?\n%s" % origin_work_file
        message_box = QtGui.QMessageBox.information(self, "Warming Tip", message_info,
                                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
        if message_box.name == "Yes":
            self.create_origin_file(origin_work_file)

    def progress_shutdown(self):
        self.progress_bar.setRange(0, 10)
        self.progress_bar.setValue(10)
        self.progress_bar.hide()

    def call_back(self, task_finished, file_name):
        if task_finished:
            self.post_publish(file_name)
            self.progress_shutdown()
            QtGui.QMessageBox.information(self, "Warming Tip", "Task create successful.")
        else:
            self.progress_shutdown()
            QtGui.QMessageBox.critical(self, "Warming Tip", "Task create fail...")

    def post_publish(self, file_name):
        user_info = None
        obj = pipeFile.PathDetails.parse_path(file_name)
        entity_type = obj.entity_type
        if entity_type == "Asset":
            asset_type_or_sequence = obj.asset_type
            asset_or_shot = obj.asset_name
        else:
            asset_type_or_sequence = obj.sequence
            asset_or_shot = obj.shot
        step = obj.step
        task = obj.task
        users = self.user_widget.list_view.get_selected()
        start_date = str(self.start_widget.selectedDate().toString("yyyy-MM-dd"))
        due_date = str(self.start_widget.selectedDate().toString("yyyy-MM-dd"))
        priority = str(self.priority_cbox.currentText())
        description = self.description_text_edit.toPlainText()
        if users:
            user_info = [self.__sg.get_user_by_name(user) for user in users]
        update_dict = dict()
        if user_info:
            update_dict.update({"task_assignees": user_info})
        if start_date:
            update_dict.update({"start_date": start_date})
        if due_date:
            update_dict.update({"due_date": due_date})
        if priority:
            update_dict.update({"sg_priority_1": priority})
        if description:
            update_dict.update({"sg_description": description})
        update_dict.update({"sg_workfile": file_name})
        update_dict.update({"sg_status_list": "rdy"})
        self.__logger.info("update: %s" % update_dict)
        current_task = self.__sg.get_current_task(entity_type, asset_type_or_sequence, asset_or_shot, step, task)
        self.__logger.info("current task: %s" % current_task)
        try:
            self.__sg.sg.update("Task", current_task["id"], update_dict)
            self.__logger.info("update task done.")
            create_filesystem_structure.create_filesystem_structure(file_name)
            self.__logger.info("create file system structure done.")
        except RuntimeError as e:
            self.__logger.error(str(e))

    def closeEvent(self, event):
        pipeHistory.set("currentProject", self.__project)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    tm = TaskManager()
    tm.show()
    app.exec_()
