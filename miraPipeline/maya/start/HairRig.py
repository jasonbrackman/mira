# -*- coding: utf-8 -*-
import os
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import save_as, quit_maya, create_reference


def main(file_name, local):
    logger = logging.getLogger("HairRig start")
    context = pipeFile.PathDetails.parse_path(file_name)
    #  reference HighRig
    high_rig_file = pipeFile.get_task_publish_file(context.project, context.entity_type, context.asset_type,
                                                   context.asset_name, "HighRig", "HighRig")
    if not os.path.isfile(high_rig_file):
        logger.error("HighRig not publish file yet.")
        if not local:
            quit_maya.quit_maya()
        return
    create_reference.create_reference(high_rig_file)
    #  save file
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    if not local:
        quit_maya.quit_maya()
