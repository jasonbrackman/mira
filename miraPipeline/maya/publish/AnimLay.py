# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya
from miraLibs.pipeLibs.pipeMaya import publish
from miraLibs.pyLibs import copy

logger = logging.getLogger("AnimLay publish")


def main(file_name):
    # open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    publish_path = context.publish_path
    # copy image and video
    publish.copy_image_and_video(context)
    logger.info("copy image and video done.")
    # copy to publish path
    copy.copy(file_name, publish_path)
    logger.info("copy to %s" % publish_path)
    # quit maya
    quit_maya.quit_maya()
