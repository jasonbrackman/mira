# -*- coding: utf-8 -*-
import os
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import new_file, quit_maya, create_reference, save_as, load_plugin
import maya.mel as mel
from miraLibs.pipeLibs.pipeMaya.hair import import_xgen_hair


def main(file_name, local):
    logger = logging.getLogger("Lookdev start")
    new_file.new_file()
    context = pipeFile.PathDetails.parse_path(file_name)
    project = context.project
    entity_type = context.entity_type
    asset_type = context.asset_type
    asset_name = context.asset_name
    # reference in Shd
    shd_publish_file = pipeFile.get_task_publish_file(project, entity_type, asset_type, asset_name, "Shd", "Shd")
    if not os.path.isfile(shd_publish_file):
        logger.info("%s is not an exist file" % shd_publish_file)
        return
    create_reference.create_reference(shd_publish_file, asset_name)
    load_plugin.load_plugin("xgenToolkit.mll")
    mel.eval("XgCreateDescriptionEditor;")
    publish_file = pipeFile.get_task_file(project, asset_type, asset_name,
                                          "Hair", "Hair", "maya_asset_publish", "")
    context = pipeFile.PathDetails.parse_path(publish_file)
    import_xgen_hair(context, "hair")
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    if not local:
        quit_maya.quit_maya()
