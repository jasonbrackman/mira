# -*- coding: utf-8 -*-
import os
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import new_file, save_as, create_reference, quit_maya


def main(file_name, local):
    logger = logging.getLogger("shd start")
    new_file.new_file()
    context = pipeFile.PathDetails.parse_path(file_name)
    project = context.project
    entity_type = context.entity_type
    asset_type = context.asset_type
    asset_name = context.asset_name
    mdl_publish_file = pipeFile.get_task_publish_file(project, entity_type, asset_type, asset_name, "HighMdl", "HighMdl")
    if not os.path.isfile(mdl_publish_file):
        logger.warning("No model file published.")
        quit_maya.quit_maya()
        return
    create_reference.create_reference(mdl_publish_file)
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    if not local:
        quit_maya.quit_maya()
