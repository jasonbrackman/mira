# -*- coding: utf-8 -*-
import os
import sys
import logging
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import miraCore
from miraLibs.pyLibs import join_path, copy
from miraFramework.screen_shot import screen_shot
from miraFramework.drag_file_widget import DragFileWidget
from miraLibs.pipeLibs import pipeFile, pipeMira
from miraPipeline.pipeline.preflight import check_gui
from miraLibs.mayaLibs import save_as, save_file
from miraPipeline.maya.playblast import playblast_turntable, playblast_shot

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

COLUMN_WIDTH = 30


def qcpublish(step):
    script_dir = miraCore.get_pipeline_dir()
    publish_dir = join_path.join_path2(script_dir, "maya", "QCPublish")
    if publish_dir not in sys.path:
        sys.path.insert(0, publish_dir)
    step_publish = "{0}_qcpublish".format(step)
    cmd_text = "import {0}; reload({0}); {0}.main()".format(step_publish)
    exec(cmd_text)


def post_qcpublish(context):
    from miraLibs.dbLibs import db_api
    from miraLibs.pipeLibs.pipeDb import task_from_db_path
    db = db_api.DbApi(context.project).db_obj
    task = task_from_db_path.task_from_db_path(db, context.work_path)
    logger.info("Current Task: %s" % task)
    if not task:
        logger.warning("No matched task")
        return
    db.update_task_status(task, "Supervisor Review")
    db.upload_thumbnail(task, context.work_image_path)
    # upload version
    not_playblast_step = pipeMira.get_studio_value(context.project, "not_playblast_step")
    if context.step in not_playblast_step:
        db.upload_version(task, file_path=context.work_path)
    else:
        db.upload_version(task, media_path=context.work_video_path, file_path=context.work_path)
    logger.info("Upload version done.")
    # update task
    db.update_file_path(task, work_file_path=context.work_path)
    logger.info("Update work file done.")


def submit_other(other_dir, files):
    if not files:
        return
    for index, f in enumerate(files):
        base_name = os.path.basename(f)
        to_other_path = join_path.join_path2(other_dir, base_name)
        copy.copy(f, to_other_path)


class TextLabel(QLabel):
    def __init__(self, text=None, parent=None):
        super(TextLabel, self).__init__(parent)
        self.text = text
        self.setText('<font face="Microsoft YaHei" size=5  text-align=center>%s</font>' % self.text)
        self.setStyleSheet("QLabel{qproperty-alignment: AlignCenter;}")


class StatusLabel(QLabel):
    def __init__(self, parent=None):
        super(StatusLabel, self).__init__(parent)
        self.set_status("waiting")
        self.setFixedSize(COLUMN_WIDTH, COLUMN_WIDTH)

    def set_status(self, status):
        icon_dir = os.path.abspath(os.path.join(__file__, "..", "icons")).replace("\\", "/")
        icon_path = os.path.join(icon_dir, "%s.png" % status).replace("\\", "/")
        pix_map = QPixmap(icon_path)
        scaled = pix_map.scaled(QSize(COLUMN_WIDTH, COLUMN_WIDTH),Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled)


class CellQCWidget(QWidget):
    def __init__(self, widget, parent=None):
        super(CellQCWidget, self).__init__(parent)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.command = None
        self.status = "start"
        self.check = QCheckBox()
        self.check.setFixedWidth(COLUMN_WIDTH)
        self.check.setChecked(True)
        self.widget = widget
        self.label = StatusLabel()
        self.label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.check)
        main_layout.addWidget(self.widget)
        main_layout.addWidget(self.label)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)
        main_layout.setStretch(2, 0)

    def set_status(self, status):
        self.status = status
        self.label.set_status(status)

    def set_mandatory(self):
        self.check.setChecked(True)
        self.check.setEnabled(False)

    def start(self):
        self.set_status("start")

    def waiting(self):
        self.set_status("waiting")

    def fail(self):
        self.set_status("fail")

    def success(self):
        self.set_status("success")

    def run(self):
        exec(self.command)


class QC(QDialog):
    def __init__(self, parent=None):
        super(QC, self).__init__(parent)
        self.setWindowTitle("QC Publish")
        self.resize(430, 550)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        screen_shot_layout = QHBoxLayout()
        self.stretch_check = QCheckBox()
        self.stretch_check.setChecked(True)
        self.stretch_check.setEnabled(False)
        self.stretch_check.setFixedWidth(COLUMN_WIDTH)
        self.screen_shot_widget = screen_shot.ThumbnailWidget()
        self.screen_shot_widget.setFixedHeight(150)
        self.screen_shot_label = StatusLabel()
        screen_shot_layout.addWidget(self.stretch_check)
        screen_shot_layout.addWidget(self.screen_shot_widget)
        screen_shot_layout.addWidget(self.screen_shot_label)
        screen_shot_layout.setStretch(0, 0)
        screen_shot_layout.setStretch(1, 1)
        screen_shot_layout.setStretch(2, 0)

        valid_file_label = TextLabel("Valid file")
        self.valid_file_widget = CellQCWidget(valid_file_label)
        self.valid_file_widget.set_mandatory()

        preflight_label = TextLabel("Preflight")
        self.preflight_widget = CellQCWidget(preflight_label)

        playblast_label = TextLabel("Playblast")
        self.playblast_widget = CellQCWidget(playblast_label)
        self.playblast_widget.set_mandatory()

        qc_label = TextLabel("Step QC")
        self.qc_widget = CellQCWidget(qc_label)
        self.qc_widget.set_mandatory()

        self.other_widget = CellQCWidget(DragFileWidget())
        self.other_widget.set_mandatory()

        post_qc_label = TextLabel("Post QC")
        self.post_qc_widget = CellQCWidget(post_qc_label)
        self.post_qc_widget.set_mandatory()

        self.submit_btn = QPushButton("Submit")

        main_layout.addLayout(screen_shot_layout)
        main_layout.addWidget(self.valid_file_widget)
        main_layout.addWidget(self.preflight_widget)
        main_layout.addWidget(self.playblast_widget)
        main_layout.addWidget(self.qc_widget)
        main_layout.addWidget(self.other_widget)
        main_layout.addWidget(self.post_qc_widget)
        main_layout.addWidget(self.submit_btn)

        self.submit_btn.clicked.connect(self.submit)

    def submit(self):
        # has screen
        self.screen_shot_label.set_status("start")
        thumbnail_path = self.screen_shot_widget.get_thumbnail_path()
        if thumbnail_path:
            self.screen_shot_label.set_status("success")
        else:
            self.screen_shot_label.set_status("fail")
            return
        # valid file
        self.valid_file_widget.start()
        context = pipeFile.PathDetails.parse_path()
        if context and context.is_local_file() and context.is_working_file():
            self.valid_file_widget.success()
        else:
            self.valid_file_widget.fail()
            return
        # if version is 000, save as 001
        if context.version == "000":
            next_version_file = context.next_version_file
            save_as.save_as(next_version_file)
            context = pipeFile.PathDetails.parse_path()
        # get path
        entity_type = context.entity_type
        work_image_path = context.work_image_path
        local_image_path = context.local_image_path
        step = context.step
        other_dir = context.other_dir
        # preflight
        if self.preflight_widget.check.isChecked():
            self.preflight_widget.start()
            result, cg = check_gui.main_for_publish()
            if result:
                cg.close()
                cg.deleteLater()
                self.preflight_widget.success()
            else:
                self.preflight_widget.fail()
                return
        # playblast
        not_playblast_step = pipeMira.get_studio_value(context.project, "not_playblast_step")
        if step in not_playblast_step:
            self.playblast_widget.check.setChecked(False)
        if self.playblast_widget.check.isChecked():
            self.playblast_widget.start()
            try:
                if entity_type == "Asset":
                    playblast_turntable.playblast_turntable()
                elif entity_type == "Shot":
                    playblast_shot.playblast_shot()
                self.playblast_widget.success()
            except RuntimeError as e:
                logger.error(str(e))
                self.playblast_widget.fail()
                return
        # copy image
        copy.copy(thumbnail_path, local_image_path)
        copy.copy(thumbnail_path, work_image_path)
        os.remove(thumbnail_path)
        # step qc
        if self.qc_widget.check.isChecked():
            self.qc_widget.start()
            try:
                qcpublish(step)
                self.qc_widget.success()
            except:
                self.qc_widget.fail()
                return
        # other
        if self.other_widget.check.isChecked():
            self.other_widget.start()
            try:
                submit_other(other_dir, self.other_widget.widget.file_list.all_items_text())
                self.other_widget.success()
            except:
                self.other_widget.fail()
                return
        # if not preflight, save current file
        if not self.preflight_widget.check.isChecked():
            save_file.save_file()
        # save as next version file
        next_version_file = context.next_version_file
        save_as.save_as(next_version_file)
        logger.info("Save to %s" % next_version_file)
        # post qc
        if self.post_qc_widget.check.isChecked():
            self.post_qc_widget.start()
            try:
                post_qcpublish(context)
                self.post_qc_widget.success()
            except:
                self.post_qc_widget.fail()
                return
        # close self and pop a message box to tell that all finished
        self.parent_win.close()
        self.parent_win.deleteLater()
        QMessageBox.information(None, "Warming Tip", "Congratulations, QC successful.")


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(QC)


if __name__ == "__main__":
    main()
