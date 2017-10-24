# -*- coding: utf-8 -*-
import logging
from miraLibs.mayaLibs import new_file, save_as, create_group, quit_maya
from miraLibs.pipeLibs import pipeFile


def main(file_name, local):
    logger = logging.getLogger("Set start")
    new_file.new_file()
    context = pipeFile.PathDetails.parse_path(file_name)
    sequence = context.sequence
    create_group.create_group("%s_env" % sequence)
    # create network node
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    if not local:
        quit_maya.quit_maya()
