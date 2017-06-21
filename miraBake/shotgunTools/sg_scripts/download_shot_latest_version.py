#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_download_shot_latest_version
# description : ''
# author      : Aaron Hui
# date        : 2015/12/28
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import sys
# Third-party modules

# Studio modules

# Local modules
import add_environ
from py_utils.get_conf_data import get_conf_data
from sg_utils.get_tk_object import get_tk_object
from get_qss_path import get_qss_path


step_dict = {'lay': 'layout', 'anim': 'animation'}


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_download_shot_latest_version_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')

os_type = sys.platform
if "win" in os_type:
    root_path = 'D:/DOWNLOAD'
else:
    root_path = "/Volumes/Promise Pegasus/DF"


class ShotgunUtility(object):
    def __init__(self):
        self.tk = get_tk_object()
        self.sg = self.tk.shotgun

    def get_all_projects(self):
        projects = self.sg.find('Project', [], ['name'])
        projects = [project['name'] for project in projects]
        return projects

    def get_project_by_name(self, project_name):
        project_info = self.sg.find_one('Project', [['name', 'is', project_name]], [])
        return project_info

    def get_sequence(self, project_name):
        project_info = self.get_project_by_name(project_name)
        sequence_filter = [['project', 'is', project_info]]
        all_sequence = self.sg.find('Sequence', sequence_filter, ['code'])
        if not all_sequence:
            return
        all_sequence_name = [sequence['code'] for sequence in all_sequence]
        all_sequence_name.sort()
        return all_sequence_name

    def get_all_shots_by_sequence(self, project_name, sequence_name):
        project_info = self.get_project_by_name(project_name)
        sequence_info = self.sg.find_one('Sequence',
                                         [['project', 'is', project_info], ['code', 'is', sequence_name]],
                                         ['shots'])
        shots = [shot for shot in sequence_info['shots'] if '_000' not in shot['name']]
        return shots

    def get_task_by_step(self, shot, step):
        task = self.sg.find_one('Task', [['entity', 'is', shot], ['sg_task_type', 'name_is', step]], ['content'])
        return task

    def get_latest_version_by_task(self, task):
        versions = self.sg.find('Version', [['sg_task', 'is', task]], ['created_at', 'sg_uploaded_movie'])
        latest_version = None
        if versions:
            for version in versions:
                if not latest_version:
                    latest_version = version
                if version['created_at'] >= latest_version['created_at']:
                    latest_version = version
            return latest_version

    def get_all_latest_version(self, project_name, sequence_name, step):
        latest_versions = list()
        shots = self.get_all_shots_by_sequence(project_name, sequence_name)
        for shot in shots:
            step_task = self.get_task_by_step(shot, step)
            latest_version = self.get_latest_version_by_task(step_task)
            if latest_version:
                latest_versions.append(latest_version)
        return latest_versions

    def download_movie(self, version, path):
        if version['sg_uploaded_movie']:
            self.sg.download_attachment(attachment=version['sg_uploaded_movie'], file_path=path)


class DownloadShotLatestVersionUI(QDialog):
    def __init__(self, parent=None):
        super(DownloadShotLatestVersionUI, self).__init__(parent)
        main_layout = QVBoxLayout(self)

        qss_path = get_qss_path()

        self.setWindowTitle('Download Shot Latest Version')
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.resize(350, 100)
        self.setStyle(QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())

        arg_layout = QGridLayout()
        project_label = QLabel('Project')
        project_label.setFixedWidth(50)
        project_label.setAlignment(Qt.AlignRight)
        self.project_cbox = QComboBox()
        sequence_label = QLabel('Sequence')
        sequence_label.setAlignment(Qt.AlignRight)
        self.sequence_cbox = QComboBox()
        self.sequence_cbox.setEditable(True)
        step_label = QLabel('Step')
        step_label.setAlignment(Qt.AlignRight)
        self.step_cbox = QComboBox()

        arg_layout.addWidget(project_label, 0, 0, 1, 1)
        arg_layout.addWidget(self.project_cbox, 0, 1, 1, 3)
        arg_layout.addWidget(sequence_label, 1, 0, 1, 1)
        arg_layout.addWidget(self.sequence_cbox, 1, 1, 1, 3)
        arg_layout.addWidget(step_label, 2, 0, 1, 1)
        arg_layout.addWidget(self.step_cbox, 2, 1, 1, 3)

        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton('Cancel')
        self.create_btn = QPushButton('Download')
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.create_btn)

        main_layout.addLayout(arg_layout)
        main_layout.addLayout(btn_layout)


class DownloadShotLatestVersion(DownloadShotLatestVersionUI):
    sg_util = ShotgunUtility()

    def __init__(self, parent=None):
        super(DownloadShotLatestVersion, self).__init__(parent)

        self.init_settings()
        self.set_signals()

    def set_signals(self):
        self.project_cbox.currentIndexChanged.connect(self.add_sequences)
        self.cancel_btn.clicked.connect(self.close)
        self.create_btn.clicked.connect(self.download)

    def init_settings(self):
        projects = self.sg_util.get_all_projects()
        self.project_cbox.addItems(projects)
        current_project = self.get_current_project()
        index = self.project_cbox.findText(current_project)
        self.project_cbox.setCurrentIndex(index)
        if index != -1:
            sequences = self.sg_util.get_sequence(current_project)
            self.sequence_cbox.addItems(sequences)

        for step in step_dict:
            self.step_cbox.addItem(step)

    def add_sequences(self, project_index):
        project_name = self.project_cbox.itemText(project_index)
        all_sequences = self.sg_util.get_sequence(str(project_name))
        self.sequence_cbox.clear()
        if all_sequences:
            self.sequence_cbox.addItems(all_sequences)

    def get_conf(self):
        conf_data = get_conf_data()
        return conf_data

    def get_current_project(self):
        conf_data = self.get_conf()
        current_project = conf_data['current_project']['current_project']
        return current_project

    def download(self):
        project_name = str(self.project_cbox.currentText())
        sequence_name = str(self.sequence_cbox.currentText())
        step = str(self.step_cbox.currentText())
        download_sequence_path = os.path.abspath(os.path.join(root_path, step_dict[step], 'seq'+sequence_name))
        if not os.path.isdir(download_sequence_path):
            os.makedirs(download_sequence_path)
        all_shots = self.sg_util.get_all_shots_by_sequence(project_name, sequence_name)
        progress_dialog = QProgressDialog('Downloading...Please wait - -', 'Cancel', 0, len(all_shots))
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()
        value = 0
        for shot in all_shots:
            progress_dialog.setValue(value)
            if progress_dialog.wasCanceled():
                break
            task = self.sg_util.get_task_by_step(shot, step)
            if not task:
                value += 1
                continue
            latest_version = self.sg_util.get_latest_version_by_task(task)
            if not latest_version:
                value += 1
                continue
            download_mov_path = os.path.join(download_sequence_path, shot['name']+'.mov')
            self.sg_util.download_movie(latest_version, download_mov_path)
            value += 1
        try:
            os.startfile(download_sequence_path)
        except:pass


def main():
    app = QApplication(sys.argv)
    dslv = DownloadShotLatestVersion()
    dslv.show()
    app.exec_()

if __name__ == "__main__":
    main()
