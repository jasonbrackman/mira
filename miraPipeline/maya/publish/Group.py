# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya
from miraLibs.pipeLibs.pipeMaya import publish

logger = logging.getLogger("Group publish")


def main(file_name):
    open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    # copy image and video
    publish.copy_image_and_video(context)
    logger.info("copy image and video done.")
    # export _MODEL group to publish path
    publish.export_need_to_publish(context)
    logger.info("Export _MODEL group to publish done.")
    # generate AD file
    publish.create_ad(context)
    # quit maya
    quit_maya.quit_maya()
