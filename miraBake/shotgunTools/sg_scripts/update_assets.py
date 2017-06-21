#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/11/30
# version     :
# usage       :
# notes       :

# Built-in modules
import sys
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *

# Third-party modules

# Studio modules

# Local modules
import add_environ
from sg_utils import get_sg


class ShotgunUtilities(object):
    def __init__(self):
        self.sg = get_sg.get_sg()
        
    def get_project(self):
        all_projects = self.sg.find('Project', [], ['name'])
        if not all_projects:
            return
        all_project_name = [project['name'] for project in all_projects]
        return all_project_name

    def get_sequence(self, project_name):
        project_id = self.sg.find_one('Project', [['name', 'is', project_name]], ['id'])['id']
        sequence_filter = [['project', 'is', {'type': 'Project', 'id': project_id}]]
        all_sequence = self.sg.find('Sequence', sequence_filter, ['code'])
        if not all_sequence:
            return
        all_sequence_name = [sequence['code'] for sequence in all_sequence]
        all_sequence_name.sort()
        return all_sequence_name

    def update_assets(self, project_name, sequence_name):
        # get sequences info
        project_id = self.sg.find_one('Project', [['name', 'is', project_name]], ['id'])['id']
        sequence_filter = [['project', 'is', {'type': 'Project', 'id': project_id}],
                           ['code', 'is', sequence_name]]
        sequence_info = self.sg.find_one('Sequence', sequence_filter, ['shots', 'code', 'id'])
        sequence_id = sequence_info['id']
        shots = sequence_info['shots']
        # get all shots
        if not shots:
            return
        # get shot 000 info
        shot_zero_name = sequence_info['code']+'_000'
        shot_zero_info = self.sg.find_one('Shot', [['code', 'is', shot_zero_name]], ['id'])
        shot_zero_id = None
        if not shot_zero_info:
            print '[AAS info]: %s is not exist in shogun' % shot_zero_name
        else:
            shot_zero_id = shot_zero_info['id']
        # get all asset  names
        all_asset_name = list()
        for shot in shots:
            shot_filter = [['id', 'is', shot['id']],
                           ['code', 'is_not', shot_zero_name]]
            shot_info = self.sg.find_one('Shot', shot_filter, ['assets'])
            if shot_info:
                assets = shot_info['assets']
                if assets:
                    for asset in assets:
                        asset_name = asset['name']
                        all_asset_name.append(asset_name)
        all_asset_name = list(set(all_asset_name))
        # get new all assets
        if not all_asset_name:
            return
        all_assets = list()
        for asset_name in all_asset_name:
            asset_filter = [['code', 'is', asset_name]]
            asset_info = self.sg.find_one('Asset', asset_filter, ['id','type'])
            all_assets.append(asset_info)
        print all_assets
        # update shot 000
        data = {'assets': all_assets}
        if shot_zero_id:
            self.sg.update('Shot', shot_zero_id, data)
            print '[AAS info]: update shot 000 successful'
        self.sg.update('Sequence', sequence_id, data)
        print '[AAS info]: update sequence successful'


class UpdateAssets(QDialog):
    shotgun_utils = ShotgunUtilities()

    def __init__(self, parent=None):
        super(UpdateAssets, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('Update Assets')
        self.resize(300, 100)
        main_layout = QVBoxLayout(self)
        project_label = QLabel('Project Name')
        project_label.setFixedWidth(90)
        project_label.setAlignment(Qt.AlignRight)
        self.project_cbox = QComboBox()
        self.project_cbox.setEditable(True)
        sequence_label = QLabel('Sequence name')
        sequence_label.setAlignment(Qt.AlignRight)
        sequence_label.setFixedWidth(90)
        self.sequence_cbox = QComboBox()
        self.sequence_cbox.setEditable(True)
        self.update_btn = QPushButton('Update Assets')

        project_layout = QHBoxLayout()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)
        sequence_layout = QHBoxLayout()
        sequence_layout.addWidget(sequence_label)
        sequence_layout.addWidget(self.sequence_cbox)
        main_layout.addLayout(project_layout)
        main_layout.addLayout(sequence_layout)
        main_layout.addWidget(self.update_btn)

        self.init_settings()
        self.set_signals()

    def init_settings(self):
        all_projects = self.shotgun_utils.get_project()
        self.project_cbox.addItems(all_projects)

    def set_signals(self):
        self.project_cbox.currentIndexChanged.connect(self.add_sequences)
        self.update_btn.clicked.connect(self.do_update)

    def add_sequences(self, project_index):
        project_name = self.project_cbox.itemText(project_index)
        all_sequences = self.shotgun_utils.get_sequence(str(project_name))
        self.sequence_cbox.clear()
        if all_sequences:
            self.sequence_cbox.addItems(all_sequences)

    def do_update(self):
        project_name = str(self.project_cbox.currentText())
        sequence_name = str(self.sequence_cbox.currentText())
        self.shotgun_utils.update_assets(project_name, sequence_name)
        QMessageBox.information(None, 'Information', 'Update Successful')


def main():
    app = QApplication(sys.argv)
    ua = UpdateAssets()
    ua.show()
    app.exec_()

if __name__ == '__main__':
    main()
