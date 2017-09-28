# -*- coding: utf-8 -*-
import os
import glob
import logging
from miraLibs.mayaLibs import new_file, save_as, quit_maya
from miraLibs.pipeLibs import pipeFile, pipeMira
from miraLibs.pipeLibs.pipeMaya import fix_frame_range
from miraLibs.mayaLibs import create_group, create_reference, set_image_size, Assembly, maya_import
from miraLibs.pipeLibs.pipeMaya.rebuild_assembly import rebuild_scene


def main(file_name, local):
    logger = logging.getLogger("LgtLay start")
    new_file.new_file()
    context = pipeFile.PathDetails.parse_path(file_name)
    save_as.save_as(file_name)
    # create Light group
    import_lights(context)
    # AR set
    rebuild_scene()
    logger.info("Rebuild scene done.")
    # switch to midmdl
    assemb = Assembly.Assembly()
    assemb.set_active("MidMdl")
    # get the AnimLay cache
    abc_files = get_cache_files(context)
    if abc_files:
        for abc_file in abc_files:
            if abc_file.endswith("env.abc"):
                continue
            namespace = os.path.splitext(os.path.basename(abc_file))[0]
            create_reference.create_reference(abc_file, namespace)
    logger.info("Reference cache done.")
    # fix frame range
    fix_frame_range.fix_frame_range(context)
    logger.info("Fix frame range done.")
    logger.info("%s publish successful!" % file_name)
    # set resolution
    resolution = pipeMira.get_resolution(context.project)
    set_image_size.set_image_size(*resolution)
    save_as.save_as(file_name)
    if not local:
        quit_maya.quit_maya()


def import_lights(context):
    light_file = pipeFile.get_task_file(context.project, context.sequence, "c000",
                                        "MainLgt", "MainLgt", "maya_shot_light", "")
    if os.path.isfile(light_file):
        maya_import.maya_import(light_file)
    else:
        create_group.create_group("Lights")


def get_cache_files(context):
    AnimLay_publish_file = pipeFile.get_task_publish_file(context.project, "Shot", context.sequence,
                                                          context.shot, "AnimLay", "AnimLay")
    AnimLay_context = pipeFile.PathDetails.parse_path(AnimLay_publish_file)
    cache_dir = AnimLay_context.cache_dir
    abc_files = glob.glob("%s/*.abc" % cache_dir)
    return abc_files
