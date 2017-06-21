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
# Third-party modules

# Studio modules
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
# Local modules
import add_environ
from sg_utils import get_tk_object
from py_utils import get_conf_path
from py_utils import conf2dict
from get_qss_path import get_qss_path

root_path = 'Q:/'
asset_types = ['character', 'prop', 'environment']

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

    def get_assets_under_sequence(self, project_name, sequence_name):
        project = self.get_project_by_name(project_name)
        sequence_info = self.sg.find_one('Sequence',
                                         [['project', 'is', project], ['code', 'is', sequence_name]], ['assets'])
        all_assets = sequence_info['assets']
        return all_assets

    def get_art_task(self, asset):
        art_task = self.sg.find_one('Task', [['sg_task_type', 'name_is', 'art'], ['entity', 'is', asset]], [])
        return art_task

    def get_latest_version(self, art_task, asset_type):
        versions = self.sg.find('Version', [['sg_task', 'is', art_task]],
                                ['created_at', 'sg_uploaded_movie', 'entity'])
        latest_version = None
        if versions:
            latest_version = None
            for version in versions:
                entity = version['entity']
                if not entity:
                    continue
                entity_info = self.sg.find_one('Asset', [['id', 'is', entity['id']]], ['sg_asset_type'])
                if entity_info['sg_asset_type'].lower() not in asset_type:
                    continue
                if not latest_version:
                    latest_version = version
                else:
                    if version['created_at'] >= latest_version['created_at']:
                        latest_version = version
        return latest_version

    def get_task_path(self, art_task):
        template_name = 'photoshop_asset_publish'
        template = self.tk.templates[template_name]
        self.tk.create_filesystem_structure("Task", art_task['id'], engine="tk-photoshop")
        context = self.tk.context_from_entity('Task', art_task['id'])
        fields = context.as_template_fields(template)
        fields['version'] = 1
        current_task_path = template.apply_fields(fields)
        return current_task_path

    def get_task_new_path(self, art_task, company_name, file_name):
        task_path = self.get_task_path(art_task)
        path = None
        try:
            path = task_path.split('_library')[-1].split('_publish')[0].replace('\\', '/').strip('/')
        except Exception, e:
            print "[AAs] Error: %s" % e
        if path:
            task_new_path = os.path.join(root_path, company_name, path, file_name)
            return task_new_path

    def download_sg_uploaded_movie(self, version, path):
        if version['sg_uploaded_movie']:
            self.sg.download_attachment(attachment=version['sg_uploaded_movie'], file_path=path)


class ExportArtUI(QDialog):
    def __init__(self, parent=None):
        super(ExportArtUI, self).__init__(parent)

        self.setWindowTitle('Export art task latest version')
        self.resize(400, 100)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        qss_path = get_qss_path()
        self.setStyle(QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())

        main_layout = QVBoxLayout(self)

        company_label = QLabel('Company')
        company_label.setFixedWidth(55)
        self.company_cbox = QComboBox()
        self.company_cbox.setEditable(True)
        self.add_company_btn = QPushButton('New')
        self.add_company_btn.setFixedWidth(40)

        company_layout = QHBoxLayout()
        company_layout.addWidget(company_label)
        company_layout.addWidget(self.company_cbox)
        company_layout.addWidget(self.add_company_btn)

        project_layout = QHBoxLayout()
        project_label = QLabel('Project')
        project_label.setFixedWidth(55)
        self.project_cbox = QComboBox()
        self.project_cbox.setEditable(True)
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        sequence_layout = QHBoxLayout()
        sequence_label = QLabel('Sequence')
        sequence_label.setFixedWidth(55)
        self.sequence_cbox = QComboBox()
        self.sequence_cbox.setEditable(True)
        sequence_layout.addWidget(sequence_label)
        sequence_layout.addWidget(self.sequence_cbox)

        type_layout = QHBoxLayout()
        type_label = QLabel('type')
        type_label.setFixedWidth(55)
        type_layout.addWidget(type_label)
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(False)
        for asset_type in asset_types:
            self.check_box = QCheckBox(asset_type)
            self.button_group.addButton(self.check_box)
            type_layout.addWidget(self.check_box)

        separator_layout = QHBoxLayout()
        separator_layout.setContentsMargins(0, 10, 0, 0)
        separator_layout.setAlignment(Qt.AlignVCenter)
        frame = QFrame()
        frame.setFrameStyle(QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111}')
        separator_layout.addWidget(frame)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.cancel_btn = QPushButton('Cancel')
        self.export_btn = QPushButton('Export')
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.export_btn)

        main_layout.addLayout(company_layout)
        main_layout.addLayout(project_layout)
        main_layout.addLayout(sequence_layout)
        main_layout.addLayout(type_layout)
        main_layout.addLayout(separator_layout)
        main_layout.addLayout(button_layout)


class ExportArt(ExportArtUI):
    sg_util = ShotgunUtility()

    def __init__(self, parent=None):
        super(ExportArt, self).__init__(parent)
        self.init_project_and_sequence()
        self.init_company()
        self.set_signals()

    def set_signals(self):
        self.add_company_btn.clicked.connect(self.add_new_company)
        self.export_btn.clicked.connect(self.do_export)
        self.project_cbox.currentIndexChanged.connect(self.add_sequences)
        self.cancel_btn.clicked.connect(self.close)

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
        text = QInputDialog.getText(None, 'Input a company', 'Please input a new company name')
        if text[0]:
            new_company_dir = os.path.join(root_path, text[0])
            if not os.path.isdir(new_company_dir):
                os.makedirs(new_company_dir)

    def get_type(self):
        types = [button.text() for button in self.button_group.buttons() if button.isChecked()]
        return types

    def do_export(self):
        current_project = self.project_cbox.currentText()
        current_sequence = self.sequence_cbox.currentText()
        company = self.company_cbox.currentText()
        asset_types = self.get_type()
        if not all((current_project, current_sequence, company)):
            raise Exception("[AAS] information: make sure company/project/sequence filled")
        assets = self.sg_util.get_assets_under_sequence(current_project, current_sequence)
        if not assets:
            raise Exception("[AAS] info: Project: %s Sequence: %s linked no asset" % (current_project, current_sequence))
        progress_dialog = QProgressDialog('Downloading...Please wait - -', 'Cancel', 0, len(assets))
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()
        value = 0
        for asset in assets:
            progress_dialog.setValue(value)
            asset_name = asset['name']
            art_task = self.sg_util.get_art_task(asset)
            if not art_task:
                value += 1
                continue
            latest_version = self.sg_util.get_latest_version(art_task, asset_types)
            if not latest_version:
                value += 1
                continue
            task_new_path = self.sg_util.get_task_new_path(art_task, company, asset_name+'.jpg')
            task_new_path = task_new_path.replace('\\', '/')
            if not os.path.isdir(os.path.dirname(task_new_path)):
                os.makedirs(os.path.dirname(task_new_path))
            try:
                self.sg_util.download_sg_uploaded_movie(latest_version, task_new_path)
                print "[AAS] info: download to %s" % task_new_path
            except Exception, e:
                print "[AAS] error: %s" % e
            value += 1
        print "\n\n[AAS] info: Download successful!"


def main():
    app = QApplication(sys.argv)
    ea = ExportArt()
    ea.show()
    app.exec_()

if __name__ == '__main__':
    main()
