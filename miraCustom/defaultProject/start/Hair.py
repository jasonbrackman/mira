# -*- coding: utf-8 -*-
import logging
import os
from miraLibs.mayaLibs import save_as, quit_maya, create_reference, create_group, new_file, create_project
from miraLibs.pipeLibs import pipeFile


def main(file_name, local):
    logger = logging.getLogger("Hair start")
    new_file.new_file()
    # copy low mdl publish file as mdl file
    context = pipeFile.PathDetails.parse_path(file_name)
    project = context.project
    entity_type = context.entity_type
    asset_type = context.asset_type
    asset_name = context.asset_name
    # reference in mdl publish file
    asset_type_short_name = context.asset_type_short_name
    mdl_publish_file = pipeFile.get_task_publish_file(project, entity_type, asset_type, asset_name, "HighMdl", "HighMdl")
    if not os.path.isfile(mdl_publish_file):
        logger.warning("No mdl file published.")
        quit_maya.quit_maya()
        return
    create_reference.create_reference(mdl_publish_file)
    # create sculp group
    sculp_group = "%s_%s_SCULP" % (asset_type_short_name, asset_name)
    create_group.create_group(sculp_group)
    if local:
        create_project.create_project(os.path.dirname(file_name))
    # create project
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    if not local:
        quit_maya.quit_maya()

