# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya
from miraLibs.pipeLibs.pipeMaya import publish
from miraLibs.pyLibs import copy


def main(file_name, local):
    logger = logging.getLogger("Group publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    # copy image and video
    publish.copy_image_and_video(context)
    logger.info("copy image and video done.")
    # copy to publish path
    copy.copy(file_name, context.publish_path)
    logger.info("Copy to publish path.")
    # generate AD file
    publish.create_ad(context)
    logger.info("Create AD done.")
    # quit maya
    if not local:
        quit_maya.quit_maya()
