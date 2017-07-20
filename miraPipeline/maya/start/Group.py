# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import save_as, quit_maya


def main(file_name):
    logger = logging.getLogger("Group start")
    # copy low mdl publish file as mdl file
    context = pipeFile.PathDetails.parse_path(file_name)
    asset_name = context.asset_name
    asset_type_short_name = context.asset_type_short_name
    model_name = "%s_%s_MODEL" % (asset_type_short_name, asset_name)
    # create default group
    mc.group(name=model_name, empty=1)
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    quit_maya.quit_maya()

