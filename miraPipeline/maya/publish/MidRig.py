# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya
from miraLibs.pipeLibs.pipeMaya import publish, rename_pipeline_shape


def main(file_name):
    logger = logging.getLogger("MidRig publish")
    open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    # copy image
    publish.copy_image_and_video(context)
    logger.info("Copy image and video done.")
    # import all reference
    publish.reference_opt()
    logger.info("Import reference done.")
    # rename shape
    if not rename_pipeline_shape.rename_pipeline_shape():
        raise RuntimeError("Rename shape error.")
    logger.info("Rename shape done.")
    # export needed
    publish.export_need_to_publish(context, "rig")
    logger.info("Export to publish path done.")
    # add to AD
    publish.add_mesh_to_ad(context)
    logger.info("Add to AD done.")
    # quit maya
    quit_maya.quit_maya()
