# -*- coding: utf-8 -*-
import os
import logging
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraLibs.mayaLibs import save_as
from miraLibs.mayaLibs import get_scene_name
from miraLibs.pipeLibs import pipeFile
from miraLibs.dbLibs import db_api
import playblast_turntable
import playblast_shot
from miraLibs.qtLibs import render_ui

OBJECT_NAME = "Playblast"


class UploadMovie(QDialog):
    def __init__(self, parent=None):
        super(UploadMovie, self).__init__(parent)
        self.setObjectName(OBJECT_NAME)
        self.setWindowTitle("Playblast")
        self.setWindowFlags(Qt.Window)
        self.resize(400, 300)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel()
        label.setText("<font size=4><b>Write some commit below:</font></b>")
        self.te = QTextEdit()
        btn_layout = QHBoxLayout()
        self.upload_btn = QPushButton("Playblast")
        btn_layout.addStretch()
        btn_layout.addWidget(self.upload_btn)
        main_layout.addWidget(label)
        main_layout.addWidget(self.te)
        main_layout.addLayout(btn_layout)
        self.upload_btn.clicked.connect(self.do_upload)

    def do_upload(self):
        description = self.te.toPlainText()
        result = upload_movie(description)
        if result:
            QMessageBox.information(None, "Warming Tip", "Upload done, congratulations.")
        self.close()


def upload_movie(description):
    logger = logging.getLogger(__name__)
    # get scene name
    scene_name = get_scene_name.get_scene_name()
    if not scene_name:
        QMessageBox.warning(None, "Warning", "Save scene first")
        return
    context = pipeFile.PathDetails.parse_path(scene_name)
    next_edition_file = context.next_edition_file
    save_as.save_as(next_edition_file)
    context = pipeFile.PathDetails.parse_path(next_edition_file)
    project = context.project
    entity_type = context.entity_type
    step = context.step
    task = context.task
    if entity_type == "Asset":
        asset_type_or_sequence = context.asset_type
        asset_or_shot = context.asset_name
        local_video_path = playblast_turntable.playblast_turntable(submit=False)
    else:
        asset_type_or_sequence = context.sequence
        asset_or_shot = context.shot
        local_video_path = playblast_shot.playblast_shot(submit=False)
    logger.info("Playblast done")
    if local_video_path and os.path.isfile(local_video_path):
        # save_as.save_as(next_version_file)
        db = db_api.DbApi(project).db_obj
        # entity_type, asset_type_or_sequence, asset_or_shot, step, task_name
        current_task = db.get_current_task(entity_type, asset_type_or_sequence, asset_or_shot, step, task)
        logger.info("Current Task: %s" % current_task)
        if not current_task:
            logger.warning("Task is None")
            return
        if db.typ == "shotgun":
            project_info = db.get_project_by_name()
            user = db.get_current_user()
            code = os.path.splitext(os.path.basename(local_video_path))[0]
            data = {'project': project_info,
                    'code': code,
                    'description': description,
                    'sg_status_list': 'rev',
                    'entity': current_task["entity"],
                    'sg_task': current_task,
                    'user': user}
            result = db.create('Version', data)
            db.upload("Version", result["id"], local_video_path, "sg_uploaded_movie")
            return True
        elif db.typ == "strack":
            db.upload_version(current_task, local_video_path, next_edition_file)
            return True
    else:
        logger.warning("May playblast wrong.")
        return False


def main():
    render_ui.render(UploadMovie)
