# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.log import Logger
log = Logger()
from miraLibs.mayaLibs import new_file, save_as, maya_import, create_group, load_plugin, create_reference, \
    import_exocortex_abc, set_image_size, quit_maya
from miraLibs.pipeLibs import pipeFile, Project
from miraLibs.pipeLibs.pipeMaya.rebuild_assembly import rebuild_scene
from miraLibs.pyLibs import json_operation
from miraLibs.pipeLibs.pipeMaya import fix_frame_range, get_assets, get_valid_camera


def main(file_name, local):
    logger = logging.getLogger("Lgt start")
    load_plugin.load_plugin("AbcImport.mll")
    load_plugin.load_plugin("MayaExocortexAlembic.mll")
    new_file.new_file()
    context = pipeFile.PathDetails.parse_path(file_name)
    save_as.save_as(file_name)
    # create Light group
    import_lights(context)
    logger.info("Import light done.")
    # rebuild scene
    rebuild_scene()
    logger.info("Rebuild scene done.")
    # rebuild asset
    rebuild_asset(context)
    logger.info("Rebuild asset done.")
    # reference camera
    reference_in_camera(context)
    # group assets
    group_assets()
    group_camera(file_name)
    # fix frame range
    fix_frame_range.fix_frame_range(context)
    logger.info("Fix frame range done.")
    # set resolution
    resolution = Project(context.project).resolution
    set_image_size.set_image_size(*resolution)
    save_as.save_as(file_name)
    logger.info("Publish done.")
    if not local:
        quit_maya.quit_maya()


def import_lights(context):
    light_file = pipeFile.get_task_file(context.project, context.sequence, "c000",
                                        "MainLgt", "MainLgt", "maya_shot_light", "")
    if os.path.isfile(light_file):
        maya_import.maya_import(light_file)
    else:
        create_group.create_group("Lights")


def get_anim_cache_dir(context):
    anim_publish_file = pipeFile.get_task_publish_file(context.project, "Shot", context.sequence,
                                                       context.shot, "Anim", "Anim")
    anim_context = pipeFile.PathDetails.parse_path(anim_publish_file)
    cache_dir = anim_context.cache_dir
    return cache_dir


def rebuild_asset(context):
    asset_info_file = pipeFile.get_task_file(context.project, context.sequence, context.shot, "Anim", "Anim",
                                             "maya_shot_assetInfo", "")
    if not os.path.isfile(asset_info_file):
        log.warning("%s is not an exist file." % asset_info_file)
        return
    asset_info_list = json_operation.get_json_data(asset_info_file)
    if not asset_info_list:
        log.warning("No data in the json file %s." % asset_info_file)
        return
    cache_dir = get_anim_cache_dir(context)
    for asset_info in asset_info_list:
        asset_type = asset_info.get("type")
        asset_name = asset_info.get("name")
        namespace = asset_info.get("namespace")
        # project, entity_type, asset_type_sequence, asset_name_shot, step, task, version="", engine="maya"
        asset_shd_file = pipeFile.get_task_publish_file(context.project, "Asset", asset_type, asset_name, "Shd", "Shd")
        if os.path.isfile(asset_shd_file):
            create_reference.create_reference(asset_shd_file, namespace, True)
            log.info("Reference in %s" % asset_shd_file)
            cache_file = "%s/%s" % (cache_dir, "%s.abc" % namespace)
            if os.path.isfile(cache_file):
                log.info("attaching...")
                try:
                    import_exocortex_abc.import_exocortex_abc(cache_file)
                except:
                    log.error("Can't attach %s." % cache_file)
            else:
                log.warning("Cache: %s is not an exist file" % cache_file)
        else:
            log.warning("Shd: %s is not an exist file")


def reference_in_camera(context):
    cache_dir = get_anim_cache_dir(context)
    camera_abc_file = "%s/%s" % (cache_dir, "camera.abc")
    if os.path.isfile(camera_abc_file):
        create_reference.create_reference(camera_abc_file)
    else:
        log.warning("%s is not an exist file" % camera_abc_file)


def group_assets():
    char_assets = get_assets.get_assets("char")
    if char_assets:
        create_group.create_group("Char")
        mc.parent(char_assets, "Char")
    prop_assets = get_assets.get_assets("prop") + get_assets.get_assets("cprop")
    if prop_assets:
        create_group.create_group("Prop")
        mc.parent(prop_assets, "Prop")
    log.info("group assets done.")


def group_camera(file_path):
    camera = get_valid_camera.get_valid_camera(file_path)
    if camera:
        create_group.create_group("Camera")
        mc.parent(camera, "Camera")
    print "group camera done."
