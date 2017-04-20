#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/12/18
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import sys
import shutil
import logging
import re
# Third-party modules

# Studio modules
from PySide import QtGui, QtCore
# Local modules
import add_environ
from sg_utils import get_tk_object
from py_utils import get_conf_path
from py_utils import conf2dict
import get_qss_path


logging.basicConfig(filename=os.path.abspath(os.path.join(os.environ["TMP"], 'lack_publish_tasks.txt')),
                    level=logging.DEBUG, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


root_path = 'Q:/'
asset_types = ['character', 'prop', 'environment']
kind_dict = {"Asset": {"task_type": ["art", "mdl", "hmdl", "rig", "txt"],
                       "type": ['character', 'prop', 'environment']},
             "Shot": {"task_type": ["pv", "lay", "anim", "lgt", "comp"]}}
download_type_list = ["Version", "PublishedFile"]


class ShotgunUtility(object):

    def __init__(self):
        self.tk = get_tk_object.get_tk_object()
        self.sg = self.tk.shotgun

    def get_all_projects(self):
        projects = self.sg.find('Project', [], ['name'])
        project_names = [project['name'] for project in projects]
        return project_names

    def get_sequence(self, project_name):
        project_id = self.sg.find_one('Project', [['name', 'is', project_name]], ['id'])['id']
        sequence_filter = [['project', 'is', {'type': 'Project', 'id': project_id}]]
        all_sequence = self.sg.find('Sequence', sequence_filter, ['code'])
        if not all_sequence:
            return
        all_sequence_name = [sequence['code'] for sequence in all_sequence]
        all_sequence_name.sort()
        return all_sequence_name

    def get_project_by_name(self, project_name):
        return self.sg.find_one('Project', [['name', 'is', project_name]], [])

    def get_sequence_info(self, project_name, sequence_name):
        project = self.get_project_by_name(project_name)
        sequence_info = self.sg.find_one('Sequence',
                                         [['project', 'is', project], ['code', 'is', sequence_name]],
                                         ['assets', "shots"])
        return sequence_info

    def get_assets_under_sequence(self, project_name, sequence_name, asset_types):
        sequence_info = self.get_sequence_info(project_name, sequence_name)
        assets = sequence_info["assets"]
        type_assets = list()
        for asset in assets:
            asset_info = self.sg.find_one("Asset", [["id", "is", asset["id"]]], ["sg_asset_type"])
            if not asset_info["sg_asset_type"].lower()in asset_types:
                continue
            type_assets.append(asset)
        return type_assets

    def get_shots_under_sequence(self, project_name, sequence_name):
        sequence_info = self.get_sequence_info(project_name, sequence_name)
        shots = sequence_info["shots"]
        return shots

    def get_task(self, entity_info, task_type):
        task = self.sg.find_one('Task',
                                [["sg_task_type", "name_is", task_type], ["entity", "is", entity_info]],
                                ['entity', "sg_task_type", "content", "sg_status_list"])
        return task

    def get_task_publish_path(self, task_info, asset_types=None):
        task_type = task_info["sg_task_type"]["name"]
        entity = task_info["entity"]
        entity_type = entity['type']
        template_name = None
        if entity_type == "Asset":
            entity_info = self.sg.find_one("Asset", [["id", "is", entity["id"]]], ["sg_asset_type"])
            if not entity_info["sg_asset_type"].lower() in asset_types:
                return
            if task_type == "art":
                template_name = "photoshop_asset_publish"
                engine = "tk-photoshop"
            elif task_type in ["mdl", "hmdl", "rig"]:
                template_name = "maya_asset_publish"
                engine = "tk-maya"
        if entity_type == "Shot":
            if task_type in ["pv", "lay", "anim", "lgt"]:
                template_name = "maya_shot_publish"
                engine = "tk-maya"
        if not template_name:
            return
        template = self.tk.templates[template_name]
        self.tk.create_filesystem_structure("Task", task_info['id'], engine=engine)
        context = self.tk.context_from_entity('Task', task_info['id'])
        fields = context.as_template_fields(template)
        fields['version'] = 1
        current_task_path = template.apply_fields(fields)
        return current_task_path

    def get_latest_publish_path(self, path, offset=0):
        if not path:
            return
        current_task_dir = os.path.dirname(path)
        if not os.path.isdir(current_task_dir):
            return
        if not os.listdir(current_task_dir):
            return
        padding_list = re.findall('_v(\d+)\.', path)
        if not padding_list:
            return
        padding = len(padding_list[0])
        path = path.replace('\\', '/')
        pattern = re.sub('_v\d{%s}\.' % padding, '_v(\d{%s})\.' % padding, path)
        # get all published versions
        versions = list()
        for published_file in os.listdir(current_task_dir):
            published_file_path = os.path.join(current_task_dir, published_file).replace('\\', '/')
            matched = re.match(pattern, published_file_path)
            if not matched:
                continue
            version_num = matched.group(1)
            versions.append(version_num)
        if versions:
            max_version = max([int(version) for version in versions])+offset
            max_version_str = '_v'+str(max_version).zfill(padding)+'.'
            publish_file_name = re.sub('_v\d{%s}\.' % padding, max_version_str, path)
            publish_file_name = os.path.abspath(publish_file_name)
            return publish_file_name, max_version

    def get_latest_version_by_task(self, task_info, asset_types=None):
        versions = self.sg.find('Version', [['sg_task', 'is', task_info]], ['created_at', 'sg_uploaded_movie', "entity"])
        if not versions:
            print "[AAS] info: %s has no version" % task_info["content"]
            return
        latest_version = None
        for version in versions:
            if not version["entity"]:
                continue
            if asset_types:
                entity = version['entity']
                entity_info = self.sg.find_one('Asset', [['id', 'is', entity['id']]], ['sg_asset_type'])
                if not entity_info["sg_asset_type"].lower() in asset_types:
                    continue
            if not latest_version:
                latest_version = version
            if version['created_at'] >= latest_version['created_at']:
                latest_version = version
        return latest_version

    def get_task_version_path(self, task_info, company_name):
        root_version_path = os.path.abspath(os.path.join(root_path, company_name, "versions"))
        entity = task_info["entity"]
        if entity["type"] == "Asset":
            asset_info = self.sg.find_one('Asset', [['id', 'is', entity['id']]], ['sg_asset_type', "code"])
            path = os.path.abspath(os.path.join(root_version_path, "assets", asset_info["sg_asset_type"],
                                                asset_info["code"], task_info["sg_task_type"]["name"],
                                                asset_info["code"]+".jpg"))
        elif entity["type"] == "Shot":
            shot_info = self.sg.find_one('Shot', [['id', 'is', entity['id']]], ["code"])
            sequence_name = shot_info["code"].split("_")[0]
            path = os.path.abspath(os.path.join(root_version_path, "shots", sequence_name,
                                                task_info["sg_task_type"]["name"],
                                                shot_info["code"]+".mov"))
        return path

    def download_sg_uploaded_movie(self, task_info, company_name, asset_types=None):
        latest_version = self.get_latest_version_by_task(task_info, asset_types)
        if not latest_version:
            return
        path = self.get_task_version_path(task_info, company_name)
        if not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        if latest_version['sg_uploaded_movie']:
            self.sg.download_attachment(attachment=latest_version['sg_uploaded_movie'], file_path=path)


class DownloadCategoryFilesUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(DownloadCategoryFilesUI, self).__init__(parent)

        self.setWindowTitle('Export art task latest version')
        self.resize(400, 100)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        qss_path = get_qss_path.get_qss_path()
        self.setStyle(QtGui.QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())

        main_layout = QtGui.QVBoxLayout(self)

        company_label = QtGui.QLabel('Company')
        company_label.setFixedWidth(65)
        self.company_cbox = QtGui.QComboBox()
        self.company_cbox.setEditable(True)
        self.add_company_btn = QtGui.QPushButton('New')
        self.add_company_btn.setFixedWidth(40)

        company_layout = QtGui.QHBoxLayout()
        company_layout.addWidget(company_label)
        company_layout.addWidget(self.company_cbox)
        company_layout.addWidget(self.add_company_btn)

        project_layout = QtGui.QHBoxLayout()
        project_label = QtGui.QLabel('Project')
        project_label.setFixedWidth(65)
        self.project_cbox = QtGui.QComboBox()
        self.project_cbox.setEditable(True)
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        sequence_layout = QtGui.QHBoxLayout()
        sequence_label = QtGui.QLabel('Sequence')
        sequence_label.setFixedWidth(65)
        self.sequence_cbox = QtGui.QComboBox()
        self.sequence_cbox.setEditable(True)
        sequence_layout.addWidget(sequence_label)
        sequence_layout.addWidget(self.sequence_cbox)

        shot_asset_layout = QtGui.QHBoxLayout()
        shot_asset_label = QtGui.QLabel("Asset/Shot")
        shot_asset_label.setFixedWidth(65)
        shot_asset_layout.addWidget(shot_asset_label)
        self.shot_asset_btn_grp = QtGui.QButtonGroup()
        for i in kind_dict:
            shot_asset_check_box = QtGui.QCheckBox(i)
            self.shot_asset_btn_grp.addButton(shot_asset_check_box)
            if i == "Asset":
                shot_asset_check_box.setChecked(True)
            shot_asset_layout.addWidget(shot_asset_check_box)

        self.attribute_layout = QtGui.QStackedLayout()
        asset_widget = QtGui.QWidget()
        asset_layout = QtGui.QVBoxLayout(asset_widget)
        # asset type layout
        asset_type_layout = QtGui.QHBoxLayout()
        asset_type_label = QtGui.QLabel("asset type")
        asset_type_label.setFixedWidth(65)
        asset_type_layout.addWidget(asset_type_label)
        self.asset_type_btn_grp = QtGui.QButtonGroup()
        self.asset_type_btn_grp.setExclusive(False)
        for i in kind_dict["Asset"]["type"]:
            asset_type_check_box = QtGui.QCheckBox(i)
            self.asset_type_btn_grp.addButton(asset_type_check_box)
            asset_type_layout.addWidget(asset_type_check_box)
        # asset_type_layout.addStretch()

        # asset task type layout
        asset_task_type_layout = QtGui.QHBoxLayout()
        asset_task_type_label = QtGui.QLabel("task type")
        asset_task_type_label.setFixedWidth(65)
        asset_task_type_layout.addWidget(asset_task_type_label)
        self.asset_task_type_btn_grp = QtGui.QButtonGroup()
        self.asset_task_type_btn_grp.setExclusive(False)
        for i in kind_dict['Asset']["task_type"]:
            asset_task_type_check_box = QtGui.QCheckBox(i)
            self.asset_task_type_btn_grp.addButton(asset_task_type_check_box)
            asset_task_type_layout.addWidget(asset_task_type_check_box)
        asset_layout.addLayout(asset_type_layout)
        asset_layout.addLayout(asset_task_type_layout)

        shot_widget = QtGui.QWidget()
        shot_layout = QtGui.QVBoxLayout(shot_widget)
        shot_task_type_layout = QtGui.QHBoxLayout()
        shot_task_type_label = QtGui.QLabel("task type")
        shot_task_type_layout.addWidget(shot_task_type_label)
        self.shot_task_type_btn_grp = QtGui.QButtonGroup()
        self.shot_task_type_btn_grp.setExclusive(False)
        for i in kind_dict["Shot"]["task_type"]:
            shot_type_check_box = QtGui.QCheckBox(i)
            self.shot_task_type_btn_grp.addButton(shot_type_check_box)
            shot_task_type_layout.addWidget(shot_type_check_box)
        shot_layout.addLayout(shot_task_type_layout)

        self.attribute_layout.addWidget(asset_widget)
        self.attribute_layout.addWidget(shot_widget)

        download_type_layout = QtGui.QHBoxLayout()
        download_type_label = QtGui.QLabel('download type')
        download_type_layout.addWidget(download_type_label)
        self.download_type_btn_grp = QtGui.QButtonGroup()
        self.download_type_btn_grp.setExclusive(False)
        for i in download_type_list:
            download_check_box = QtGui.QCheckBox(i)
            self.download_type_btn_grp.addButton(download_check_box)
            download_type_layout.addWidget(download_check_box)

        separator_layout = QtGui.QHBoxLayout()
        separator_layout.setContentsMargins(0, 10, 0, 0)
        separator_layout.setAlignment(QtCore.Qt.AlignVCenter)
        frame = QtGui.QFrame()
        frame.setFrameStyle(QtGui.QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111}')
        separator_layout.addWidget(frame)

        button_layout = QtGui.QHBoxLayout()
        button_layout.addStretch()
        self.cancel_btn = QtGui.QPushButton('Cancel')
        self.export_btn = QtGui.QPushButton('Export')
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.export_btn)

        main_layout.addLayout(company_layout)
        main_layout.addLayout(project_layout)
        main_layout.addLayout(sequence_layout)
        main_layout.addLayout(shot_asset_layout)
        main_layout.addLayout(self.attribute_layout)
        main_layout.addLayout(download_type_layout)
        main_layout.addLayout(separator_layout)
        main_layout.addLayout(button_layout)


class DownloadCategoryFiles(DownloadCategoryFilesUI):
    sg_util = ShotgunUtility()

    def __init__(self, parent=None):
        super(DownloadCategoryFiles, self).__init__(parent)
        self.init_project_and_sequence()
        self.init_company()
        self.set_signals()

    def set_signals(self):
        self.add_company_btn.clicked.connect(self.add_new_company)
        self.export_btn.clicked.connect(self.do_export)
        self.project_cbox.currentIndexChanged.connect(self.add_sequences)
        self.cancel_btn.clicked.connect(self.close)
        self.shot_asset_btn_grp.buttonClicked.connect(self.switch_shot_asset_layout)

    def get_current_project(self):
        conf_path = get_conf_path.get_conf_path()
        sg_ini_path = os.path.join(conf_path, 'sg.ini')
        conf_dict = conf2dict.conf2dict(sg_ini_path)
        return conf_dict['current_project']['current_project']

    def init_project_and_sequence(self):
        # init project
        projects = self.sg_util.get_all_projects()
        self.project_cbox.addItems(projects)
        current_project = self.get_current_project()
        index = self.project_cbox.findText(current_project)
        self.project_cbox.setCurrentIndex(index)
        # init sequence
        sequences = self.sg_util.get_sequence(current_project)
        self.sequence_cbox.addItems(sequences)

    def add_sequences(self, project_index):
        project_name = self.project_cbox.itemText(project_index)
        all_sequences = self.sg_util.get_sequence(str(project_name))
        self.sequence_cbox.clear()
        if all_sequences:
            self.sequence_cbox.addItems(all_sequences)

    def init_company(self):
        all_companies = [folder for folder in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, folder))]
        self.company_cbox.addItems(all_companies)

    def add_new_company(self):
        text = QtGui.QInputDialog.getText(None, 'Input a company', 'Please input a new company name')
        if not text:
            return
        new_company_dir = os.path.join(root_path, text[0])
        if not os.path.isdir(new_company_dir):
            os.makedirs(new_company_dir)
        self.company_cbox.addItem(text[0])
        index = self.company_cbox.findText(text[0])
        self.company_cbox.setCurrentIndex(index)

    def switch_shot_asset_layout(self):
        if self.shot_asset_btn_grp.checkedButton().text() == "Asset":
            self.attribute_layout.setCurrentIndex(0)
        else:
            self.attribute_layout.setCurrentIndex(1)

    def get_download_kind(self):
        kind = self.shot_asset_btn_grp.checkedButton().text()
        return kind

    def get_asset_download_info(self):
        asset_types = [button.text() for button in self.asset_type_btn_grp.buttons() if button.isChecked()]
        asset_task_type = [button.text() for button in self.asset_task_type_btn_grp.buttons() if button.isChecked()]
        return asset_types, asset_task_type

    def get_shot_download_info(self):
        shot_task_types = [button.text() for button in self.shot_task_type_btn_grp.buttons() if button.isChecked()]
        return 0, shot_task_types

    def get_download_info(self):
        kind = self.get_download_kind()
        if kind == "Asset":
            download_info = self.get_asset_download_info()
        else:
            download_info = self.get_shot_download_info()
        return download_info

    def get_total_kinds(self, current_project, current_sequence, asset_types=None):
        kind = self.get_download_kind()
        if kind == "Shot":
            total_kinds = self.sg_util.get_shots_under_sequence(current_project, current_sequence)
        else:
            total_kinds = self.sg_util.get_assets_under_sequence(current_project, current_sequence, asset_types)
        return total_kinds

    def download(self, download_type, task_info, company_name, sequence_name, asset_types):
        if download_type == "Version":
            self.sg_util.download_sg_uploaded_movie(task_info, company_name, asset_types)
        else:
            task_publish_path = self.sg_util.get_task_publish_path(task_info, asset_types)
            latest_publish_path = self.sg_util.get_latest_publish_path(task_publish_path, offset=0)
            if not latest_publish_path:
                print "[AAS] info: %s has no publish file" % task_info["content"]
                logging.info("[AAS] info: Sequence:%s, Task:%s has no publish file" % (sequence_name, task_info["content"]))
                return
            same_path = os.path.splitdrive(latest_publish_path[0])[1]
            same_path = same_path.replace("\\", "/")
            same_path = same_path.strip("/")
            new_path = os.path.join(root_path, company_name, same_path)
            new_dir = os.path.dirname(new_path)
            if not os.path.isdir(new_dir):
                os.makedirs(new_dir)
            else:
                for f in os.listdir(new_dir):
                    file_name = os.path.abspath(os.path.join(new_dir, f))
                    if os.path.isfile(file_name):
                        os.remove(file_name)
            shutil.copy(latest_publish_path[0], new_path)

    def do_export(self):
        current_project = self.project_cbox.currentText()
        current_sequence = self.sequence_cbox.currentText()
        company = self.company_cbox.currentText()
        download_info = self.get_download_info()
        download_type = self.download_type_btn_grp.checkedButton().text()
        if not all((current_project, current_sequence, company, download_type)):
            raise Exception("[AAS] error: make sure company/project/sequence/download type filled")
        if not download_info[1]:
            raise Exception("[AAS] error: make sure task type/type filled")
        total_kinds = self.get_total_kinds(current_project, current_sequence, download_info[0])
        tasks = [self.sg_util.get_task(entity, task_type) for entity in total_kinds for task_type in download_info[1]]
        if not tasks:
            print "[AAS] info: %s has no choose task" % current_sequence
            return
        # progress dialog
        progress_dialog = QtGui.QProgressDialog('Downloading...Please wait - -', 'Cancel', 0, len(tasks))
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.show()
        value = 0
        for task in tasks:
            progress_dialog.setValue(value)
            if not task:
                value += 1
                continue
            if task["sg_status_list"] == "hld":
                value += 1
                continue
            try:
                self.download(download_type, task, company, current_sequence, download_info[0])
            except Exception as e:
                print "[AAS] error: %s" % e
            value += 1
        print "Download finished"


def main():
    app = QtGui.QApplication(sys.argv)
    ea = DownloadCategoryFiles()
    ea.show()
    app.exec_()


if __name__ == '__main__':
    main()
