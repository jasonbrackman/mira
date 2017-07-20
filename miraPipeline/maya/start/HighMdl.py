# -*- coding: utf-8 -*-
import logging
import os
from miraLibs.mayaLibs import open_file, save_as, quit_maya
from miraLibs.pipeLibs import pipeFile


def main(file_name):
    logger = logging.getLogger("HighMdl start")
    # copy low mdl publish file as mdl file
    context = pipeFile.PathDetails.parse_path(file_name)
    project = context.project
    entity_type = context.entity_type
    asset_type = context.asset_type
    asset_name = context.asset_name
    MidMdl_publish_file = pipeFile.get_task_publish_file(project, entity_type, asset_type, asset_name, "MidMdl", "MidMdl")
    logger.info("MidMdl publish file: %s" % MidMdl_publish_file)
    if not os.path.isfile(MidMdl_publish_file):
        logger.warning("No MidMdl file published.")
        quit_maya.quit_maya()
        return
    open_file.open_file(MidMdl_publish_file)
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    quit_maya.quit_maya()
