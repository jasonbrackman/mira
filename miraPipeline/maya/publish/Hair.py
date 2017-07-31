# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import get_model_name, publish
from miraLibs.mayaLibs import open_file, quit_maya, export_abc, Xgen


logger = logging.getLogger("Hair publish")


def main(file_name):
    open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    hair_cache_path = context.abc_cache_path
    hair_path = context.hair_path
    asset_name = context.asset_name
    # copy image
    publish.copy_image_and_video(context)
    logger.info("Copy image done.")
    # export SCULP group to abc
    model_name = get_model_name.get_model_name("hair")
    export_abc.export_abc(1, 1, hair_cache_path, model_name)
    logger.info("Export abc done.")
    # export xgen file
    collection_node = str("%s_collection" % asset_name)
    xgen = Xgen.Xgen()
    xgen.export_palette(collection_node, hair_path)
    logger.info("Export .xgen file done.")
    quit_maya.quit_maya()
