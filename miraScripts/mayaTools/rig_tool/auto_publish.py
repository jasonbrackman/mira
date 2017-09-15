# -*- coding: utf-8 -*-
import os
import logging
from Qt.QtWidgets import *
from miraLibs.mayaLibs import get_scene_name, save_file, new_file
from miraLibs.osLibs import get_parent_win
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import publish
from miraLibs.dbLibs import db_api
from miraLibs.pipeLibs.pipeDb import task_from_db_path
from miraFramework.screen_shot import screen_shot
from miraFramework.message_box import MessageWidget

logger = logging.getLogger("Rig auto publish")
PARENT_WIN = get_parent_win.get_parent_win()


def auto_publish(context, change_task_status):
    # copy image
    publish.copy_image_and_video(context)
    logger.info("Copy image and video done.")
    # import all reference
    publish.reference_opt()
    logger.info("Import reference done.")
    # export needed
    publish.export_need_to_publish(context)
    logger.info("Export to publish path done.")
    # add to AD
    publish.add_mesh_to_ad(context)
    logger.info("Add to AD done.")
    # post publish
    post_publish(context, change_task_status)
    # open current file
    new_file.new_file()


def post_publish(context, change_task_status=False):
    if not os.path.isfile(context.publish_path):
        logger.error("Something wrong with publish")
        return
    # set task publish file
    logger.info("start post publish...")
    db = db_api.DbApi(context.project).db_obj
    current_task = task_from_db_path.task_from_db_path(db, context.work_path)
    logger.info("Current Task: %s" % current_task)
    if os.path.isfile(context.image_path):
        db.upload_thumbnail(current_task, context.image_path)
    db.update_file_path(current_task, publish_file_path=context.publish_path)
    logger.info("update task publish file: %s" % context.publish_path)
    # change task status
    if change_task_status:
        db.update_task_status(current_task, "Delivered")
        logger.info("update task status: Delivered")
    # # for shotgun register publish file
    # self.logger.info("publish path: %s" % self.context.publish_path)
    # try:
    #     tk = toolkit.Toolkit(self.project).tk_obj
    #     self.logger.info("%s" % repr(tk.get_context_from_path(self.context.publish_path)))
    #     tk.publish_file(self.context.publish_path)
    # except RuntimeError as e:
    #     self.logger.error(str(e))
    logger.info("All Done.")


class AutoPublish(QDialog):
    def __init__(self, parent=None):
        super(AutoPublish, self).__init__(parent)
        self.setObjectName("Auto Publish")
        self.setWindowTitle("Auto Publish")
        self.resize(500, 400)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.thumbnail_widget = screen_shot.ThumbnailWidget()
        self.check = QCheckBox("Change current task status to Delivered")
        self.check.setChecked(True)
        btn_layout = QHBoxLayout()
        self.publish_btn = QPushButton("Publish")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addStretch()
        btn_layout.addWidget(self.publish_btn)
        btn_layout.addWidget(self.cancel_btn)
        main_layout.addWidget(self.thumbnail_widget)
        main_layout.addWidget(self.check)
        main_layout.addLayout(btn_layout)
        self.set_signals()

    @property
    def set_final(self):
        if self.check.isChecked():
            return True
        else:
            return False

    def set_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        self.publish_btn.clicked.connect(self.do_publish)

    def do_publish(self):
        scene_name = get_scene_name.get_scene_name()
        save_file.save_file()
        context = pipeFile.PathDetails.parse_path(scene_name)
        if context.step not in ["MidRig", "HighRig"]:
            mw = MessageWidget("Warning", "This step is not Rig step", PARENT_WIN)
            mw.show()
            return
        # save image to image path
        pixmap = self.thumbnail_widget._get_thumbnail()
        if not pixmap:
            mw = MessageWidget("Warning", "Screen shot first!", PARENT_WIN)
            mw.show()
            return
        image_dir = os.path.dirname(context.image_path)
        if not os.path.isdir(image_dir):
            os.makedirs(image_dir)
        pixmap.save(context.image_path)
        # auto_publish
        auto_publish(context, self.set_final)
        self.close()
        mw = MessageWidget("Success", "Auto Publish done.", PARENT_WIN)
        mw.show()


def main():
    import maya.cmds as mc
    if mc.window("Auto Publish", q=1, exists=1):
        mc.deleteUI("Auto Publish")
    ap = AutoPublish(PARENT_WIN)
    ap.show()
