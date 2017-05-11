#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_export_abc_for_fx
# description : ''
# author      : HeShuai
# date        : 2016/1/12
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
import sys
import re
import subprocess
# Third-party modules

from PySide import QtGui, QtCore
# Studio modules

# Local modules
import add_environ
import miraLibs.sgLibs.sgUtility as aas_sg
reload(aas_sg)
from miraLibs.pyLibs.conf2dict import conf2dict
from parse_shot import parse_shot
from utility.py_utils import get_path_utility


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_export_abc_for_fx_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')

fx_cache_dir = 'Z:/Resource/Fxcache'


def convert(title_color, info_type, info_color, origin_string):
    new_string = '<font color={title_color} size=4>[AAS] {type}:</font><font color={info_color}>{info}</font>'
    new_string = new_string.format(title_color=title_color, type=info_type, info_color=info_color, info=origin_string)
    return new_string


def convert_error_info(origin_string):
    new_string = convert('#FF0000', "error", "#FF0000", origin_string)
    return new_string


def convert_tip_info(origin_string):
    new_string = convert("#00FF00", 'info', "#FFFFFF", origin_string)
    return new_string


def convert_warning_info(origin_string):
    new_string = convert("#F0E68C", 'warning', "#FFFFFF", origin_string)
    return new_string


def get_qss_path():
    current_path = __file__
    current_dir = os.path.dirname(current_path)
    qss_path = os.path.join(os.path.join(current_dir, "style.qss"))
    return qss_path


class RunCommandTread(QtCore.QThread):
    progress_signal = QtCore.Signal(int)
    info_signal = QtCore.Signal(basestring)
    detail_signal = QtCore.Signal(basestring)

    def __init__(self, command_list=None, parent=None):
        super(RunCommandTread, self).__init__(parent)
        self.command_list = command_list

        self.finished.connect(self.show_finish_info)

    def show_finish_info(self):
        self.info_signal.emit("<font color=#00FF00 size=4><b>All tasks are finished</b></font>")

    def run(self):
        value = 2
        self.progress_signal.emit(value)
        for command in self.command_list:
            command_info = convert_tip_info("Running command \"%s\"" % command)
            self.detail_signal.emit("@@clear@@")
            self.detail_signal.emit(command)
            self.info_signal.emit("<font color=#00FF00>%s</font>" % command_info)
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while True:
                return_code = p.poll()
                if return_code == 0:
                    break
                elif return_code == 1:
                    command_info = "%s was terminated for some reason." % command
                    self.info_signal.emit(convert_error_info(command_info))
                    break
                    # raise Exception(convert_error_info(command_info))
                elif return_code is not None:
                    command_info = "exit return code is: %s" % str(return_code)
                    self.info_signal.emit(convert_error_info(command_info))
                    break
                    # raise Exception(convert_error_info(command_info))
                line = p.stdout.readline()
                if line.strip():
                    self.detail_signal.emit(line)
                    if line.startswith("[AAS] error"):
                        self.info_signal.emit("<font color=#FF0000>%s</font>" % line)
                    if line.startswith("[AAS] warning"):
                        self.info_signal.emit("<font color=#F0E68C>%s</font>" % line)
            value += 1
            self.progress_signal.emit(value)


class TextEditWidget(QtGui.QWidget):
    def __init__(self, title=None, parent=None):
        super(TextEditWidget, self).__init__(parent)
        self.title = title
        main_layout = QtGui.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_group = QtGui.QGroupBox()
        main_layout.addWidget(main_group)
        main_group.setTitle(self.title)
        group_layout = QtGui.QHBoxLayout(main_group)
        group_layout.setContentsMargins(5, 5, 5, 5)
        self.text_edit = QtGui.QLineEdit()
        self.text_edit.setPlaceholderText(u"输入格式:001_002,002_001-002_005,003_*")
        self.text_edit.selectAll()
        group_layout.addWidget(self.text_edit)


class ExportAbcForFxUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ExportAbcForFxUI, self).__init__(parent)

        qss_path = get_qss_path()

        self.resize(500, 500)
        self.setWindowTitle("Fx export abc tool")
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setStyle(QtGui.QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())

        main_layout = QtGui.QVBoxLayout(self)
        # main_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        main_layout.setAlignment(QtCore.Qt.AlignTop)

        project_layout = QtGui.QHBoxLayout()
        project_label = QtGui.QLabel('Project')
        project_label.setFixedWidth(40)
        self.project_cbox = QtGui.QComboBox()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        self.lay_widget = TextEditWidget("lay", self)
        self.anim_widget = TextEditWidget("anim", self)

        button_layout = QtGui.QHBoxLayout()
        self.force_checkbox = QtGui.QCheckBox("force")
        self.cancel_btn = QtGui.QPushButton('Cancel')
        self.export_btn = QtGui.QPushButton('Export')
        button_layout.addWidget(self.force_checkbox)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.export_btn)

        progress_layout = QtGui.QHBoxLayout()
        progress_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setTextVisible(False)
        progress_layout.addWidget(self.progress_bar)

        self.info_widget = QtGui.QTabWidget()
        self.info_tb = QtGui.QTextBrowser()
        self.has_export_tb = QtGui.QTextBrowser()
        self.detail_tb = QtGui.QTextBrowser()
        self.info_widget.addTab(self.info_tb, "Information")
        self.info_widget.addTab(self.has_export_tb, "exported")
        self.info_widget.addTab(self.detail_tb, "Detail")

        main_layout.addLayout(project_layout)
        # main_layout.addWidget(format_tb)
        main_layout.addWidget(self.lay_widget)
        main_layout.addWidget(self.anim_widget)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(progress_layout)
        main_layout.addWidget(self.info_widget)


class ExportAbcForFx(ExportAbcForFxUI):
    def __init__(self, parent=None):
        super(ExportAbcForFx, self).__init__(parent)
        self.conf_dir = os.path.join(os.path.dirname(__file__), 'conf')
        self.sg_utils = aas_sg.SgUtility()

        self.__set_signals()
        self.__init_ui()

    def __set_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        self.export_btn.clicked.connect(self.export)

    def __init_ui(self):
        projects = self.sg_utils.get_all_projects()
        projects = [project.lower() for project in projects]
        self.project_cbox.addItems(projects)
        current_project = self.__get_current_project()
        current_project_index = self.project_cbox.findText(current_project)
        if current_project_index != -1:
            self.project_cbox.setCurrentIndex(current_project_index)

    def __get_current_project(self):
        project_conf_path = os.path.join(self.conf_dir, 'project.ini')
        project_dict = conf2dict(project_conf_path)
        current_project = project_dict['project']['current_project']
        return current_project

    def __get_filled_shots(self, text_edit):
        current_project = str(self.project_cbox.currentText())
        filled_string = str(text_edit.text())
        if not filled_string:
            return
        parse_result = parse_shot(filled_string, current_project)
        return parse_result

    def get_lay_filled_shots(self):
        parse_result = self.__get_filled_shots(self.lay_widget.text_edit)
        if isinstance(parse_result, list):
            lay_shots = parse_result
            return lay_shots
        elif isinstance(parse_result, basestring):
            self.info_tb.append(convert_error_info(parse_result))

    def get_anim_filled_shots(self):
        parse_result = self.__get_filled_shots(self.anim_widget.text_edit)
        if isinstance(parse_result, list):
            anim_shots = parse_result
            return anim_shots
        elif isinstance(parse_result, basestring):
            self.info_tb.append(convert_error_info(parse_result))

    def get_export_files(self):
        current_project = str(self.project_cbox.currentText())
        no_published_task = list()
        need_export_files = list()
        lay_shot_task_names = list()
        anim_shot_task_names = list()
        lay_shots = self.get_lay_filled_shots()
        anim_shots = self.get_anim_filled_shots()
        if not (lay_shots or anim_shots):
            return
        if lay_shots:
            lay_shot_task_names = ["%s_lay" % shot for shot in lay_shots]
        if anim_shots:
            anim_shot_task_names = ["%s_anim" % shot for shot in anim_shots]
        all_task_names = lay_shot_task_names + anim_shot_task_names
        all_task_names.sort()
        for task_name in all_task_names:
            task_info = self.sg_utils.get_task_info_by_task_name(current_project, task_name)
            if not task_info:
                self.info_tb.append(convert_warning_info("Has no task %s" % task_name))
                continue
            published_version_info = self.sg_utils.get_latest_published_of_task(current_project, task_name)
            if not published_version_info:
                no_published_task.append(task_name)
            else:
                if self.force_checkbox.isChecked():
                    need_export_files.append(published_version_info[0])
                else:
                    published_version_number = published_version_info[1]
                    print "%s published Version number %s" % (task_name, published_version_number)
                    abc_version_number = self.__get_abc_latest_version(current_project, task_name)
                    print "%s abc_version_number %s" % (task_name, abc_version_number)
                    if published_version_number > abc_version_number:
                        need_export_files.append(published_version_info[0])
                    elif published_version_number == abc_version_number:
                        self.has_export_tb.append(
                            convert_warning_info("%s ---has exported abc (version: v%s)" %
                                                 (task_name, str(published_version_number).zfill(3))))
                    else:
                        self.has_export_tb.append(
                            convert_warning_info("%s ---has exported latest version abc (version: v%s)" %
                                                 (task_name, str(abc_version_number).zfill(3))))
        if no_published_task:
            self.info_tb.append(convert_warning_info("no published task"))
            self.info_tb.append("<font color=#FFFFFF>%s</font>" % str(no_published_task))
        return need_export_files

    def export(self):
        self.info_tb.clear()
        self.has_export_tb.clear()
        self.detail_tb.clear()
        self.progress_bar.setValue(2)
        command_list = self.__get_command_list()
        if not command_list:
            self.info_tb.append(convert_error_info("Has no command to run"))
            return
        self.progress_bar.setRange(2, len(command_list)+2)
        self.threads = list()
        thread = RunCommandTread(command_list)
        thread.progress_signal.connect(self.set_progress)
        thread.info_signal.connect(self.append_information)
        thread.detail_signal.connect(self.append_detail)
        thread.start()
        self.threads.append(thread)

    def set_progress(self, value):
        self.progress_bar.setValue(value)

    def append_information(self, value):
        self.info_tb.append(value)

    def append_detail(self, value):
        self.detail_tb.append(value)
        if value == "@@clear@@":
            self.detail_tb.clear()

    def __get_command_list(self):
        command_list = list()
        need_export_files = self.get_export_files()
        need_export_files.sort()
        if not need_export_files:
            self.info_tb.append(convert_warning_info("No export files"))
            return
        self.info_tb.append(convert_tip_info("need export files: \n\t%s" % need_export_files))
        export_abc_script_path = self.__get_export_abc_script_path()
        for export_file in need_export_files:
            print export_file
            export_file = export_file.replace("\\", '/')
            sg_shot_info = self.sg_utils.get_shot_info_by_maya_file_path(export_file)
            if not sg_shot_info:
                self.info_tb.append(convert_error_info("Can't find entity from path %s" % export_file))
                continue
            if not sg_shot_info["type"] == "Shot":
                self.info_tb.append(convert_error_info("%s entity is not a shot" % export_file))
                continue
            frame_range = self.sg_utils.get_frame_range_by_shot(sg_shot_info)
            start_frame, end_frame = frame_range
            if not all((start_frame, end_frame)):
                self.info_tb.append(convert_error_info("%s has no frame range" % export_file))
            abc_file_dir = self.__get_abc_dir_by_maya_file_path(export_file)
            if not abc_file_dir:
                continue
            log_file_path = os.path.abspath(os.path.join(abc_file_dir, "log.txt"))
            log_file_path = log_file_path.replace('\\', '/')
            mayabatch = get_path_utility.get_maya_batch(export_file)
            command = "\"%s\" -log \"%s\" -command \"python \\\"abc_file='%s';" \
                      "abc_start=%s;abc_end=%s;abc_output='%s';execfile('%s')\\\"\"" % \
                      (mayabatch, log_file_path, export_file, start_frame-50, end_frame,
                       abc_file_dir, export_abc_script_path)
            command_list.append(command)
        return command_list

    def __get_abc_latest_version(self, project_name, task_name):
        version_number = -1
        sequence_name = task_name.split('_')[0]
        shot_name = task_name.split('_')[1]
        step = task_name.split('_')[2]
        abc_dir = os.path.abspath(os.path.join(fx_cache_dir, project_name, "source", sequence_name, shot_name, step))
        if not os.path.isdir(abc_dir):
            return version_number
        version_pattern = "v(\d+)"
        latest_version = None
        for version in os.listdir(abc_dir):
            version_number_list = re.findall(version_pattern, version)
            if not version_number_list:
                continue
            temp_version_number = int(version_number_list[0])
            if not latest_version:
                latest_version = temp_version_number
            if temp_version_number > latest_version:
                latest_version = temp_version_number
        return latest_version

    def __get_abc_dir_by_maya_file_path(self, maya_file_path):
        base_name = os.path.basename(maya_file_path)
        base_pattern = r'^\w+_\d+_\d+_\w+_v\d+\.[ma|mb]'
        if not re.match(base_pattern, base_name):
            self.info_tb.append(convert_error_info("%s is not a valid path" % maya_file_path))
            return
        base_name_split = base_name.split('_')
        project_name = base_name_split[0]
        sequence_name = base_name_split[1]
        shot_name = base_name_split[2]
        step = base_name_split[3]
        version_name = base_name_split[4].split('.')[0]
        abc_file_dir = os.path.abspath(os.path.join(fx_cache_dir,
                                                    project_name, "source", sequence_name,
                                                    shot_name, step, version_name))
        abc_file_dir = abc_file_dir.replace("\\", '/')
        return abc_file_dir

    def __get_export_abc_script_path(self):
        current_path = __file__
        export_abc_script_path = os.path.abspath(os.path.join(os.path.dirname(current_path), "export_abc.py"))
        export_abc_script_path = export_abc_script_path.replace('\\', '/')
        return export_abc_script_path


def main():
    app = QtGui.QApplication(sys.argv)
    eaf = ExportAbcForFx()
    eaf.show()
    app.exec_()


def maya_main():
    import mayakit
    eaf = ExportAbcForFx(mayakit.get_maya_win("PySide"))
    eaf.show()


if __name__ == "__main__":
    main()
