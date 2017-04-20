#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/12/23
# version     :
# usage       :
# notes       :

# Built-in modules
import time
import sys
import os
from PySide import QtGui, QtCore

# Third-party modules

# Studio modules

# Local modules
import add_environ
from sg_utils.get_tk_object import get_tk_object
from sg_utils.get_shotgun_login import get_shotgun_login
from py_utils.get_conf_data import get_conf_data
from get_qss_path import get_qss_path


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
        task = self.sg.find_one('Task', [['entity', 'is', shot], ['sg_task_type', 'name_is', step]], ['content', 'task_assignees'])
        return task

    def get_latest_version_by_task(self, task):
        versions = self.sg.find('Version', [['sg_task', 'is', task]], ['created_at'])
        latest_version = None
        if versions:
            for version in versions:
                if not latest_version:
                    latest_version = version
                if version['created_at'] >= latest_version['created_at']:
                    latest_version = version
            return latest_version

    def message(self, information_text):
        QtGui.QMessageBox.information(None, 'Information', information_text)

    def get_all_versions(self, project_name, sequence_name, step):
        # get all shots by sequence
        shots = self.get_all_shots_by_sequence(project_name, sequence_name)
        if not shots:
            information_text = 'There is no shot under project %s sequence %s' \
                               % (project_name, sequence_name)
            self.message(information_text)
            return
        # get all step tasks
        all_step_task = list()
        for shot in shots:
            step_task = self.get_task_by_step(shot, step)
            if step_task:
                all_step_task.append(step_task)
        if not all_step_task:
            information_text = 'There is no task under project %s sequence %s step %s' \
                                            % (project_name, sequence_name, step)
            self.message(information_text)
            return
        # get all latest versions
        versions = list()
        information = 'These tasks has no version: \n\n'
        for task in all_step_task:
            latest_version = self.get_latest_version_by_task(task)
            if not latest_version:
                assign_to = ''
                if task['task_assignees']:
                    for user in task['task_assignees']:
                        assign_to += user['name']
                else:
                    assign_to = ''
                information += task['content']+ '          '+'Assign to:'+assign_to+'\n'
                continue
            versions.append(latest_version)
        return versions, information

    def get_user(self):
        user_name = get_shotgun_login()
        user = self.sg.find_one('HumanUser', [['login', 'is', user_name]], ['login'])
        return user

    def get_playlist_by_name(self, playlist_name):
        playlist = self.sg.find_one('Playlist', [['code', 'is', playlist_name]], [])
        return playlist

    def create_playlist(self, project_name, playlist_name, versions):
        project_info = self.get_project_by_name(project_name)
        user = self.get_user()
        data = {'code': playlist_name,
                'project': project_info,
                'versions': versions,
                'created_by': user
                }
        self.sg.create('Playlist', data)

    def update_playlist(self, playlist, versions):
        data = {'versions': versions}
        self.sg.update(playlist['type'], playlist['id'], data)


class CreatePlaylistUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(CreatePlaylistUI, self).__init__(parent)

        qss_path = get_qss_path()
        self.setStyle(QtGui.QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())
        self.setWindowTitle('Create Playlist')
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.resize(350, 100)

        main_layout = QtGui.QVBoxLayout(self)

        arg_layout = QtGui.QGridLayout()
        project_label = QtGui.QLabel('Project')
        project_label.setFixedWidth(50)
        project_label.setAlignment(QtCore.Qt.AlignRight)
        self.project_cbox = QtGui.QComboBox()
        sequence_label = QtGui.QLabel('Sequence')
        sequence_label.setAlignment(QtCore.Qt.AlignRight)
        self.sequence_cbox = QtGui.QComboBox()
        self.sequence_cbox.setEditable(True)
        step_label = QtGui.QLabel('Step')
        step_label.setAlignment(QtCore.Qt.AlignRight)
        self.step_cbox = QtGui.QComboBox()
        part_label = QtGui.QLabel('Part Name')
        part_label.setAlignment(QtCore.Qt.AlignRight)
        self.part_le = QtGui.QLineEdit()
        arg_layout.addWidget(project_label, 0, 0, 1, 1)
        arg_layout.addWidget(self.project_cbox, 0, 1, 1, 3)
        arg_layout.addWidget(sequence_label, 1, 0, 1, 1)
        arg_layout.addWidget(self.sequence_cbox, 1, 1, 1, 3)
        arg_layout.addWidget(step_label, 2, 0, 1, 1)
        arg_layout.addWidget(self.step_cbox, 2, 1, 1, 3)
        arg_layout.addWidget(part_label, 3, 0, 1, 1)
        arg_layout.addWidget(self.part_le, 3, 1, 1, 3)

        btn_layout = QtGui.QHBoxLayout()
        self.cancel_btn = QtGui.QPushButton('Cancel')
        self.create_btn = QtGui.QPushButton('Create Playlist')
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.create_btn)

        main_layout.addLayout(arg_layout)
        main_layout.addLayout(btn_layout)


class CreatePlaylist(CreatePlaylistUI):
    sg_util = ShotgunUtility()

    def __init__(self, parent=None):
        super(CreatePlaylist, self).__init__(parent)

        self.init_settings()
        self.set_signals()

    def set_signals(self):
        self.project_cbox.currentIndexChanged.connect(self.add_sequences)
        self.cancel_btn.clicked.connect(self.close)
        self.create_btn.clicked.connect(self.do_create)

    def init_settings(self):
        projects = self.sg_util.get_all_projects()
        self.project_cbox.addItems(projects)
        current_project = self.get_current_project()
        index = self.project_cbox.findText(current_project)
        self.project_cbox.setCurrentIndex(index)
        if index != -1:
            sequences = self.sg_util.get_sequence(current_project)
            self.sequence_cbox.addItems(sequences)
        # init step
        shot_step_list = self.get_step_list()
        self.step_cbox.addItems(shot_step_list)

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

    def get_step_list(self):
        conf_data = self.get_conf()
        shot_step = conf_data['shot_step']['shot_step']
        shot_step_list = shot_step.split(',')
        return shot_step_list

    def do_create(self):
        project_name = str(self.project_cbox.currentText())
        sequence_name = str(self.sequence_cbox.currentText())
        step = str(self.step_cbox.currentText())
        part = str(self.part_le.text())
        if not all((project_name, sequence_name, step)):
            return
        now = time.localtime(time.time())
        current_time = time.strftime("%Y_%m_%d", now)
        if part:
            playlist_name = '%s_%s_%s_%s_%s' % (project_name, sequence_name, step, current_time, part)
        else:
            playlist_name = '%s_%s_%s_%s' % (project_name, sequence_name, step, current_time)
        playlist = self.sg_util.get_playlist_by_name(playlist_name)
        version_list = self.sg_util.get_all_versions(project_name, sequence_name, step)
        print "[AAS] versions: %s" % str(version_list)
        if playlist:
            self.sg_util.update_playlist(playlist, version_list[0])
            print "[AAS] info: update successful"
        else:
            self.sg_util.create_playlist(project_name, playlist_name, version_list[0])
            print "[AAS] info: create successful"
        if len(version_list[1]) > 30:
            self.sg_util.message(version_list[1].decode("utf8"))


def main():
    app = QtGui.QApplication(sys.argv)
    cp = CreatePlaylist()
    cp.show()
    app.exec_()


if __name__ == '__main__':
    main()
