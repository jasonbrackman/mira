# -*- coding: utf-8 -*-
import os
import logging
from Qt.QtWidgets import *
from miraLibs.mayaLibs import open_file, get_scene_name
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import publish
from miraLibs.dbLibs import db_api
from miraLibs.pipeLibs.pipeDb import task_from_db_path

logger = logging.getLogger("Rig auto publish")


def auto_publish():
    scene_name = get_scene_name.get_scene_name()
    context = pipeFile.PathDetails.parse_path(scene_name)
    if context.step not in ["MidRig", "HighRig"]:
        return
    message_box = QMessageBox.information(None, "Warming Tip",
                                          "Do you want to change current task status to Delivered ?",
                                          QMessageBox.Yes | QMessageBox.Cancel)
    change_task_status = True if message_box.name == "Yes" else False
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
    open_file.open_file(scene_name)
    QMessageBox(None, "Warming Tip", "Publish done.")


def post_publish(context, change_task_status=False):
    if not os.path.isfile(context.publish_path):
        logger.error("Something wrong with publish")
        return
    # set task sg_publishfile
    logger.info("start post publish...")
    db = db_api.DbApi(context.project).db_obj
    current_task = task_from_db_path.task_from_db_path(db, context.work_path)
    logger.info("Current Task: %s" % current_task)
    db.update_file_path(current_task, publish_file_path=context.publish_path)
    logger.info("update task sg_publishfile: %s" % context.publish_path)
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
