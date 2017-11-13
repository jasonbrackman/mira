# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
from miraLibs.mayaLibs import new_file, save_as, create_group, quit_maya, Assembly
from miraLibs.pipeLibs import pipeFile


def main(file_name, local):
    logger = logging.getLogger("MainLgt start")
    new_file.new_file()
    create_group.create_group("Lights")
    # AR set AD file
    context = pipeFile.PathDetails.parse_path(file_name)
    project = context.project
    sequence = context.sequence
    set_ad_file = pipeFile.get_task_file(project, sequence, "c000", "Set", "Set", "maya_shot_definition", "")
    assemb = Assembly.Assembly()
    node = assemb.reference_ad("%s_c000_set" % sequence, set_ad_file)
    create_group.create_group("Env")
    mc.parent(node, "Env")
    # set Shd active
    assemb.set_active("Shd")
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    if not local:
        quit_maya.quit_maya()
