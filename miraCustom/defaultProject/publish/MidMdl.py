# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya
from miraLibs.pipeLibs.pipeMaya import publish


def main(file_name, local):
    logger = logging.getLogger("MidMdl publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path()
    publish.copy_image_and_video(context)
    logger.info("copy image and video done.")
    publish.export_need_to_publish(context)
    logger.info("export to publish done.")
    publish.export_model_to_abc(context)
    logger.info("export to abc done")
    publish.create_ad(context)
    logger.info("create ad done")
    # quit maya
    if not local:
        quit_maya.quit_maya()
