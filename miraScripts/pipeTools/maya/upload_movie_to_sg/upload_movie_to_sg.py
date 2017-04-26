# -*- coding: utf-8 -*-
import os
import logging
from PySide import QtGui, QtCore
import maya.cmds as mc
from miraLibs.mayaLibs import get_maya_win, save_as
from miraLibs.mayaLibs import get_scene_name
from miraLibs.pipeLibs import pipeFile
from miraLibs.sgLibs import Sg
from miraScripts.pipeTools.maya.playblast import playblast_turntable
from miraScripts.pipeTools.maya.playblast import playblast_shot

OBJECT_NAME = "Upload Movie"


class UploadMovie(QtGui.QDialog):
    def __init__(self, parent=None):
        super(UploadMovie, self).__init__(parent)
        self.setObjectName(OBJECT_NAME)
        self.setWindowTitle("Upload Movie to Shotgun")
        self.setWindowFlags(QtCore.Qt.Window)
        self.resize(400, 300)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        label = QtGui.QLabel()
        label.setText("<font size=4><b>Write some commit below:</font></b>")
        self.te = QtGui.QTextEdit()
        btn_layout = QtGui.QHBoxLayout()
        self.upload_btn = QtGui.QPushButton("Upload")
        btn_layout.addStretch()
        btn_layout.addWidget(self.upload_btn)
        main_layout.addWidget(label)
        main_layout.addWidget(self.te)
        main_layout.addLayout(btn_layout)
        self.upload_btn.clicked.connect(self.do_upload)

    def do_upload(self):
        description = self.te.toPlainText()
        upload_movie(description)
        self.close()
        QtGui.QMessageBox.information(None, "Warming Tip", "Upload done, congratulations.")


def upload_movie(description):
    logger = logging.getLogger(__name__)
    # get scene name
    scene_name = get_scene_name.get_scene_name()
    if not scene_name:
        QtGui.QMessageBox.warning(None, "Warning", "Save scene first")
        return
    obj = pipeFile.PathDetails.parse_path(scene_name)
    project = obj.project
    entity_type = obj.entity_type
    step = obj.step
    task = obj.task
    next_version_file = obj.next_version_file
    if entity_type == "Asset":
        asset_type_or_sequence = obj.asset_type
        asset_or_shot = obj.asset_name
        video_path = playblast_turntable.playblast_turntable()
    else:
        asset_type_or_sequence = obj.sequence
        asset_or_shot = obj.shot
        video_path = playblast_shot.playblast_shot()
    logger.info("Playblast done")
    if video_path and os.path.isfile(video_path):
        save_as.save_as(next_version_file)
        sg = Sg.Sg(project)
    # entity_type, asset_type_or_sequence, asset_or_shot, step, task_name
        current_task = sg.get_current_task(entity_type, asset_type_or_sequence, asset_or_shot, step, task)
        logger.info("Current Task: %s" % current_task)
        if not current_task:
            logger.warning("Task is None")
            return
        project_info = sg.get_project_by_name()
        user = sg.get_current_user()
        code = os.path.splitext(os.path.basename(video_path))[0]
        data = {'project': project_info,
                'code': code,
                'description': description,
                'sg_status_list': 'rev',
                'entity': current_task["entity"],
                'sg_task': current_task,
                'user': user}
        result = sg.sg.create('Version', data)
        sg.sg.upload("Version", result["id"], video_path, "sg_uploaded_movie")
    else:
        logger.warning("May playblast wrong.")


def main():
    if mc.window(OBJECT_NAME, q=1, ex=1):
        mc.deleteUI(OBJECT_NAME)
    um = UploadMovie(get_maya_win.get_maya_win("PySide"))
    um.show()
