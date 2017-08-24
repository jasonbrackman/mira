# -*- coding: utf-8 -*-
import os
import logging
import imp
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import miraCore
from miraLibs.pyLibs import join_path, copy
from miraFramework.screen_shot import screen_shot
from miraFramework.drag_file_widget import DragFileWidget
from miraFramework.message_box import MessageWidget
from miraLibs.pipeLibs import pipeFile, pipeMira
from miraPipeline.pipeline.preflight import check_gui
from miraLibs.mayaLibs import save_as, save_file
from miraPipeline.maya.playblast import playblast_turntable, playblast_shot
from miraLibs.osLibs import get_parent_win

PARENT_WIN = get_parent_win.get_parent_win()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

COLUMN_WIDTH = 30


def qcpublish(step):
    script_dir = miraCore.get_pipeline_dir()
    qcpublish_dir = join_path.join_path2(script_dir, "maya", "QCPublish")
    fn_, path, desc = imp.find_module(step, [qcpublish_dir])
    mod = imp.load_module(step, fn_, path, desc)
    mod.main()


def post_qcpublish(context, version_file):
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
    db.upload_version(task, media_path=version_file, file_path=context.work_path)
    logger.info("Upload version done.")
    # update task
    db.update_file_path(task, work_file_path=context.work_path)
    db.update_task(task, current_version=int(context.version))
    logger.info("Update work file done.")


def submit_other(other_dir, files):
    if not files:
        return
    for index, f in enumerate(files):
        base_name = os.path.basename(f)
        to_other_path = join_path.join_path2(other_dir, base_name)
        copy.copy(f, to_other_path)


def submit_version():
    pass


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
        raise RuntimeError("Something wrong with this step")

    def success(self):
        self.set_status("success")

    def run(self):
        exec(self.command)


class QC(QDialog):
    def __init__(self, parent=None):
        super(QC, self).__init__(parent)
        self.setWindowTitle("QC Publish")
        self.resize(430, 600)
        self.context = pipeFile.PathDetails.parse_path()
        self.project = self.context.project
        self.entity_type = self.context.entity_type
        self.work_image_path = self.context.work_image_path
        self.local_image_path = self.context.local_image_path
        self.step = self.context.step
        self.other_dir = self.context.other_dir
        self.video_path = self.context.work_video_path
        self.next_version_file = self.context.next_version_file
        self.not_playblast_step = pipeMira.get_studio_value(self.project, "not_playblast_step")
        self.not_submit_version_step = pipeMira.get_studio_value(self.project, "not_submit_version_step")
        self.has_playblast = self.step not in self.not_playblast_step
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        screen_shot_layout = QHBoxLayout()
        self.stretch_check = QCheckBox()
        self.stretch_check.setChecked(True)
        self.stretch_check.setEnabled(False)
        self.stretch_check.setFixedWidth(COLUMN_WIDTH)
        self.screen_shot_widget = screen_shot.ThumbnailWidget()
        self.screen_shot_widget.setFixedHeight(180)
        self.screen_shot_label = StatusLabel()
        screen_shot_layout.addWidget(self.stretch_check)
        screen_shot_layout.addWidget(self.screen_shot_widget)
        screen_shot_layout.addWidget(self.screen_shot_label)
        screen_shot_layout.setStretch(0, 0)
        screen_shot_layout.setStretch(1, 1)
        screen_shot_layout.setStretch(2, 0)

        preflight_label = TextLabel("Preflight")
        self.preflight_widget = CellQCWidget(preflight_label)

        playblast_label = TextLabel("Playblast")
        self.playblast_widget = CellQCWidget(playblast_label)
        self.playblast_widget.set_mandatory()

        version_layout = QVBoxLayout()
        version_layout.setContentsMargins(0, 10, 0, 10)
        version_label = QLabel("<font color=#ff9c00><b>审核（只限一个文件）</b></font>")
        self.version_widget = CellQCWidget(DragFileWidget())
        self.version_widget.set_mandatory()
        version_layout.addWidget(version_label)
        version_layout.addWidget(self.version_widget)

        qc_label = TextLabel("Step QC")
        self.qc_widget = CellQCWidget(qc_label)
        self.qc_widget.set_mandatory()

        other_layout = QVBoxLayout()
        other_layout.setContentsMargins(0, 10, 0, 10)
        other_label = QLabel("<font color=#ff9c00><b>Other</b></font>")
        self.other_widget = CellQCWidget(DragFileWidget())
        self.other_widget.set_mandatory()
        other_layout.addWidget(other_label)
        other_layout.addWidget(self.other_widget)

        post_qc_label = TextLabel("Post QC")
        self.post_qc_widget = CellQCWidget(post_qc_label)
        self.post_qc_widget.set_mandatory()

        self.submit_btn = QPushButton("Submit")

        main_layout.addLayout(screen_shot_layout)
        main_layout.addWidget(self.preflight_widget)
        if self.has_playblast:
            main_layout.addWidget(self.playblast_widget)
        else:
            main_layout.addLayout(version_layout)
        main_layout.addWidget(self.qc_widget)
        main_layout.addLayout(other_layout)
        main_layout.addWidget(self.post_qc_widget)
        main_layout.addWidget(self.submit_btn)

        self.submit_btn.clicked.connect(self.submit)

    def submit_screen_shot(self):
        self.screen_shot_label.set_status("start")
        thumbnail_path = self.screen_shot_widget.get_thumbnail_path()
        if thumbnail_path:
            self.screen_shot_label.set_status("success")
            return thumbnail_path
        else:
            self.screen_shot_label.set_status("fail")

    def submit_preflight(self):
        if self.preflight_widget.check.isChecked():
            self.preflight_widget.start()
            result, cg = check_gui.main_for_publish()
            if result:
                cg.close()
                cg.deleteLater()
                self.preflight_widget.success()
                return True
            else:
                self.preflight_widget.fail()
                return False
        else:
            return None

    def submit_version(self, thumbnail_path=None):
        if self.has_playblast:
            self.playblast_widget.start()
            try:
                if self.entity_type == "Asset":
                    playblast_turntable.playblast_turntable()
                elif self.entity_type == "Shot":
                    playblast_shot.playblast_shot()
                self.playblast_widget.success()
                return self.video_path
            except RuntimeError as e:
                logger.error(str(e))
                self.playblast_widget.fail()
        else:
            if self.step in self.not_submit_version_step:
                return
            version_files = self.version_widget.widget.file_list.all_items_text()
            if len(version_files) > 1:
                QMessageBox.warning(None, "Warming Tip", "Only one file can submit once a time.")
                self.version_widget.fail()
                return
            # if version files, copy to video path, match the ext
            elif len(version_files) == 1:
                origin_file = version_files[0]
            else:
                origin_file = thumbnail_path
            try:
                ext = os.path.splitext(origin_file)[-1]
                version_file = "%s%s" % (os.path.splitext(self.video_path)[0], ext)
                copy.copy(origin_file, version_file)
                self.version_widget.success()
                return version_file
            except:
                self.version_widget.fail()

    def submit_step_qc(self):
        self.qc_widget.start()
        try:
            qcpublish(self.step)
            self.qc_widget.success()
        except:
            self.qc_widget.fail()

    def submit_other(self):
        self.other_widget.start()
        try:
            submit_other(self.other_dir, self.other_widget.widget.file_list.all_items_text())
            self.other_widget.success()
        except:
            self.other_widget.fail()

    def submit_post(self, version_file):
        self.post_qc_widget.start()
        try:
            post_qcpublish(self.context, version_file)
            self.post_qc_widget.success()
        except:
            self.post_qc_widget.fail()

    def submit(self):
        # has screen
        thumbnail_path = self.submit_screen_shot()
        if not thumbnail_path:
            return
        # preflight
        preflight_status = self.submit_preflight()
        if preflight_status is not None:
            if not preflight_status:
                return
        # playblast
        version_file = self.submit_version(thumbnail_path)
        if (self.step not in self.not_submit_version_step) and (not version_file):
            return
        # copy image
        copy.copy(thumbnail_path, self.local_image_path)
        copy.copy(thumbnail_path, self.work_image_path)
        os.remove(thumbnail_path)
        # step qc
        self.submit_step_qc()
        # other
        self.submit_other()
        # if not preflight, save current file
        if not self.preflight_widget.check.isChecked():
            save_file.save_file()
        # save as next version file
        save_as.save_as(self.next_version_file)
        logger.info("Save to %s" % self.next_version_file)
        # post qc
        self.submit_post(version_file)
        # close self and pop a message box to tell that all finished
        self.close()
        self.deleteLater()
        QMessageBox.information(None, "Warming Tip", "Congratulations, QC successful.")


def main():
    context = pipeFile.PathDetails.parse_path()
    if context and context.is_local_file() and context.is_working_file():
        qc = QC(PARENT_WIN)
        qc.show()
    else:
        mw = MessageWidget("Warning", "This file is not a valid file.Please check it ^ ^", PARENT_WIN)
        mw.show()


if __name__ == "__main__":
    main()
