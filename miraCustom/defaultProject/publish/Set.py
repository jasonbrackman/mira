# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya
from miraLibs.pipeLibs.pipeMaya import publish
from miraLibs.pyLibs import copy


def main(file_name, local):
    logger = logging.getLogger("sceneset publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    publish_path = context.publish_path
    # copy to publish path
    copy.copy(file_name, publish_path)
    logger.info("Copy to publish path done.")
    # copy image and video
    publish.copy_image_and_video(context)
    # create AD file
    publish.create_shot_ad(context)
    logger.info("Create AD done.")
    # quit maya
    if not local:
        quit_maya.quit_maya()
