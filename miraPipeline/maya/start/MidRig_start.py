# -*- coding: utf-8 -*-
import os
import logging
import optparse
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import new_file, save_as, create_reference, create_group, quit_maya


def main():
    logger = logging.getLogger("MidRig start")
    context = pipeFile.PathDetails.parse_path(options.file)
    project = context.project
    asset_type = context.asset_type
    asset_type_short_name = context.asset_type_short_name
    asset_name = context.asset_name
    MidMdl_publish_file = pipeFile.get_asset_task_publish_file(project, asset_type, asset_name, "MidMdl", "MidMdl")
    if not os.path.isfile(MidMdl_publish_file):
        logger.warning("No MidMdl file published.")
        quit_maya.quit_maya()
        return
    new_file.new_file()
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
        create_group.create_group(model_name, "Geometry")
    elif asset_type == "Prop":
        rig_group_name = "%s_%s_RIG" % (asset_type_short_name, asset_name)
        create_group.create_group(model_name, root_group_name)
        create_group.create_group(rig_group_name)
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
    save_as.save_as(options.file)
    logger.info("%s publish successful!" % options.file)
    quit_maya.quit_maya()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="maya file ma or mb.", metavar="string")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    options, args = parser.parse_args()
    if len([i for i in ["file_name"] if i in dir()]) == 1:
        options.file = file_name
        main()
