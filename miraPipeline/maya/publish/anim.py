# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya
from miraLibs.pipeLibs.pipeMaya import publish, rebuild_assembly
from miraLibs.pyLibs import copy


def main(file_name, local):
    logger = logging.getLogger("AnimLay publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    publish_path = context.publish_path
    # copy image and video
    publish.copy_image_and_video(context)
    logger.info("Copy image and video done.")
    # copy to publish path
    copy.copy(file_name, publish_path)
    logger.info("Copy to %s" % publish_path)
    # write out assembly edits
    rebuild_assembly.export_scene()
    logger.info("Export assembly edits done.")
    # export cache
    publish.export_cache(context)
    logger.info("Export cache done.")
    # export asset info

    # quit maya
    if not local:
        quit_maya.quit_maya()
