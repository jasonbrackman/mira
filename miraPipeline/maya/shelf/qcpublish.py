# -*- coding: utf-8 -*-
import os
import logging
import sys
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import miraCore
from miraLibs.pyLibs import join_path
from miraLibs.pipeLibs import pipeFile
from miraPipeline.pipeline.preflight import check_gui
from miraLibs.pipeLibs.pipeMaya import screen_shot
from miraLibs.mayaLibs import get_maya_win, save_as
from miraLibs.pipeLibs.copy import Copy
from miraFramework.FileListWidget import FileListWidget


maya_window = get_maya_win.get_maya_win()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OtherDialog(QDialog):
    def __init__(self, other_dir=None, parent=None):
        super(OtherDialog, self).__init__(parent)
        self.other_dir = other_dir
        self.setup_ui()
        self.set_signals()

    def set_signals(self):
        self.submit_btn.clicked.connect(self.do_submit)

    def setup_ui(self):
        self.resize(600, 400)
        self.setWindowTitle("Submit Others")
        self.label = QLabel()
        self.label.setText("<font size=4 color=#ff8c00><b>Drag files below:</b></font>")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.file_list = FileListWidget()
        submit_layout = QHBoxLayout()
        self.submit_btn = QPushButton("Submit")
        submit_layout.addStretch()
        submit_layout.addWidget(self.submit_btn)
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.file_list)
        main_layout.addLayout(submit_layout)
        main_layout.addWidget(self.progress_bar)

    def do_submit(self):
        files = self.file_list.all_items_text()
        if not files:
            self.close()
            return
        self.progress_bar.show()
        self.progress_bar.setRange(0, len(files))
        for index, f in enumerate(files):
            base_name = os.path.basename(f)
            to_other_path = join_path.join_path2(self.other_dir, base_name)
            Copy.copy(f, to_other_path)
            self.progress_bar.setValue(index+1)
        self.close()


class ProgressDialog(QProgressDialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        self.setRange(1, 100)
        self.setWindowTitle("QCPublish")
        # self.setWindowModality(Qt.WindowModal)
        self.setMinimumWidth(600)
        self.canceled.connect(break_down)

    def set_text(self, label_text):
        self.setLabelText(label_text)

    def set_value(self, value):
        self.setValue(value)
        
    def show_up(self):
        self.set_value(10)
        self.show()


def break_down():
    raise Exception("Exit.")


def qcpublish_screen_shot(entity_type, image_path):
    if entity_type == "Asset":
        screen_shot_object = screen_shot.ScreenShot(image_path, False)
        screen_shot_object.screen_shot()
    else:
        return
        # screen_shot_object = screen_shot.ScreenShot(image_path, True)
    # screen_shot_object.screen_shot()


def qcpublish(step):
    script_dir = miraCore.get_pipeline_dir()
    publish_dir = join_path.join_path2(script_dir, "maya", "QCPublish")
    if publish_dir not in sys.path:
        sys.path.insert(0, publish_dir)
    step_publish = "{0}_qcpublish".format(step)
    cmd_text = "import {0}; reload({0}); {0}.{0}()".format(step_publish)
    exec(cmd_text)


def post_qcpublish(obj):
    from miraLibs.dbLibs import db_api
    from miraLibs.pipeLibs.pipeDb import task_from_db_path
    db = db_api.DbApi(obj.project).db_obj
    task = task_from_db_path.task_from_db_path(db, obj.work_path)
    if not task:
        logger.warning("No matched task")
        return
    db.update_task_status(task, "First Review")
    db.upload_thumbnail(task, obj.image_path)


def main():
    message_box = QMessageBox.information(None, "Warming Tip", "Do you want to publish this task.",
                                                QMessageBox.Yes | QMessageBox.No)
    if message_box.name == "No":
        return
    try:
        obj = pipeFile.PathDetails.parse_path()
    except:
        logger.warning("Name Error.")
        return
    # check is local file
    if not obj.is_local_file():
        QMessageBox.warning(None, "Warning", "This file is not a local work file.\n Permission defined.")
        return
    # check if work file
    if not obj.is_working_file():
        QMessageBox.warning(None, "Warning", "This file is not a work file.")
        return
    progress_dialog = ProgressDialog(maya_window)
    progress_dialog.show_up()
    # preflight
    progress_dialog.set_text("Preflight checking...")
    result, cg = check_gui.main_for_publish()
    if result:
        cg.close()
        cg.deleteLater()
    else:
        logger.error("Some checks can not be passed.")
        progress_dialog.close()
        return
    progress_dialog.set_value(30)
    # save as next version file
    next_version_file = obj.next_version_file
    save_as.save_as(next_version_file)
    logger.info("Save to %s" % next_version_file)
    progress_dialog.set_value(40)
    # get path
    obj = pipeFile.PathDetails.parse_path(next_version_file)
    project = obj.project
    entity_type = obj.entity_type
    image_path = obj.image_path
    local_image_path = obj.local_image_path
    step = obj.step
    other_dir = obj.other_dir
    # copy to _other
    od = OtherDialog(other_dir, maya_window)
    od.exec_()
    progress_dialog.set_value(50)
    logger.info("Copy to others")
    # screen shot
    progress_dialog.set_text("Screen shot")
    qcpublish_screen_shot(entity_type, local_image_path)
    Copy.copy(local_image_path, image_path)
    logger.info("PreQCPublish successful.")
    progress_dialog.set_value(60)
    # post publish
    progress_dialog.set_text("%s_QCPublish" % step)
    qcpublish(step)
    logger.info("QCPublish successful.")
    progress_dialog.set_value(85)
    # write root task id to database
    progress_dialog.set_text("Add to database.")
    post_qcpublish(obj)
    logger.info("PostQCPublish successful.")
    # pop message
    progress_dialog.set_value(100)
    QMessageBox.information(maya_window, "Warming Tip", "QC publish successful.")


if __name__ == "__main__":
    pass
