# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import new_file, save_as, create_reference, create_group, quit_maya


def main(file_name, local):
    logger = logging.getLogger("MidRig start")
    new_file.new_file()
    context = pipeFile.PathDetails.parse_path(file_name)
    project = context.project
    entity_type = context.entity_type
    asset_type = context.asset_type
    asset_type_short_name = context.asset_type_short_name
    asset_name = context.asset_name
    task = context.task
    MidMdl_publish_file = pipeFile.get_task_publish_file(project, entity_type, asset_type, asset_name, "MidMdl", "MidMdl")
    if not os.path.isfile(MidMdl_publish_file):
        logger.warning("No MidMdl file published.")
        quit_maya.quit_maya()
        return
    create_reference.create_reference(MidMdl_publish_file)
    model_name = "%s_%s_MODEL" % (asset_type_short_name, asset_name)
    # create root group
    root_group_name = "%s_%s_ROOT" % (asset_type_short_name, asset_name)
    create_group.create_group(root_group_name)
    # create _BLENDS group
    blends_group = "_BLENDS"
    create_group.create_group(blends_group)
    if asset_type == "Character":
        rig_group_name = "Grp_Master_Ctl"
        create_group.create_group("Others", root_group_name)
        create_group.create_group("Geometry", root_group_name)
        create_group.create_group(model_name, blends_group)
    elif asset_type in ["Prop", "Cprop"]:
        rig_group_name = "%s_%s_RIG" % (asset_type_short_name, asset_name)
        create_group.create_group(model_name, root_group_name)
        create_group.create_group(rig_group_name)
        if asset_type in ["Prop", "Building"]:
            bounding = mc.xform(model_name, q=1, bb=1)
            max_value = max(abs(bounding[0]), abs(bounding[2]), abs(bounding[3]), abs(bounding[5]))
            radius = max_value*1.1
            center = mc.xform(model_name, q=1, sp=1, ws=1)
            circle_list = mc.circle(c=center, nr=[0, 1, 0], r=radius, name="%s_%s_Ctl" % (asset_type_short_name, asset_name))
            circle_name = circle_list[0]
            constraint_parent = mc.parentConstraint(circle_name, model_name, maintainOffset=True)
            constraint_scale = mc.scaleConstraint(circle_name, model_name, maintainOffset=True)
            mc.parent(constraint_parent, rig_group_name)
            mc.parent(constraint_scale, rig_group_name)
            mc.parent(circle_name, rig_group_name)
    create_group.create_group(rig_group_name, root_group_name)
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    if not local:
        quit_maya.quit_maya()
