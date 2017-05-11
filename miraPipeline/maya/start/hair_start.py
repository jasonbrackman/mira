# -*- coding: utf-8 -*-
import optparse
import logging
import os
import maya.cmds as mc
from miraLibs.mayaLibs import save_as, quit_maya, create_reference, create_group, load_plugin
from miraLibs.pipeLibs import pipeFile


def main():
    logger = logging.getLogger("mdl start")
    # copy low mdl publish file as mdl file
    obj = pipeFile.PathDetails.parse_path(options.file)
    project = obj.project
    asset_type = obj.asset_type
    asset_name = obj.asset_name
    asset_type_short_name = obj.asset_type_short_name
    yeti_name = "%s_%s_pgYetiMaya" % (asset_type_short_name, asset_name)
    create_yeti_node(asset_type_short_name, asset_name)
    mdl_publish_file = pipeFile.get_asset_task_publish_file(project, asset_type, asset_name, "mdl", "mdl")
    if not os.path.isfile(mdl_publish_file):
        logger.warning("No mdl file published.")
        quit_maya.quit_maya()
        return
    create_reference.create_reference(mdl_publish_file)
    create_hair_group(asset_type_short_name, asset_name)
    save_as.save_as(options.file)
    logger.info("%s publish successful!" % options.file)
    quit_maya.quit_maya()


def create_hair_group(asset_type, asset_name):
    hair_grp_name = "%s_%s_HAIR" % (asset_type, asset_name)
    hair_system_name = "%s_%s_hairsystem_grp" % (asset_type, asset_name)
    hair_rig_name = "%s_%s_hair_rig_grp" % (asset_type, asset_name)
    hair_curve_name = "%s_%s_hair_curve_grp" % (asset_type, asset_name)
    hair_render_name = "%s_%s_hair_render_grp" % (asset_type, asset_name)
    create_group.create_group(hair_grp_name)
    for grp in [hair_system_name, hair_rig_name, hair_curve_name, hair_render_name]:
        create_group.create_group(grp, hair_grp_name)


def create_yeti_node(asset_type, asset_name):
    # load yeti plugin
    load_plugin.load_plugin("pgYetiMaya.mll")
    yeti_name = "%s_%s_body_pgYetiMaya" % (asset_type, asset_name)
    node = mc.createNode("pgYetiMaya")
    transform_node = mc.listRelatives(node, p=1)[0]
    mc.rename(transform_node, yeti_name)
    yeti_group_name = "%s_%s_yetiNode" % (asset_type, asset_name)
    create_group.create_group(yeti_group_name)
    create_group.create_group(yeti_name, yeti_group_name)


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
