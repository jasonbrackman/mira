# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import get_model_name
from miraLibs.mayaLibs import open_file, quit_maya, hierarchy_opt
from miraLibs.pipeLibs.pipeMaya import publish


def main(file_name, local):
    logger = logging.getLogger("HighMdl publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    asset_type = context.asset_type
    # copy image and video
    publish.copy_image_and_video(context)
    logger.info("copy image and video done.")
    # export _MODEL group to publish path
    publish.export_need_to_publish(context)
    logger.info("Export _MODEL group to publish done.")
    # export abc cache
    publish.export_model_to_abc(context)
    logger.info("Export abc done.")
    # write out topology
    if asset_type in ["Character", "Prop", "Cprop"]:
        # write out topology
        topology_path = context.topology_path
        model_name = get_model_name.get_model_name()
        ho = hierarchy_opt.HierarchyOpt(model_name)
        ho.write_out(topology_path)
        logger.info("write out topology done.")
    # add to AD file
    publish.add_gpu_to_ad(context)
    logger.info("Add to AD done.")
    # quit maya
    if not local:
        quit_maya.quit_maya()
