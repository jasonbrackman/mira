# -*- coding: utf-8 -*-
import optparse
import os
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import get_children_file, get_latest_version_dir, yml_operation
from miraLibs.mayaLibs import create_reference, save_file, load_plugin, quit_maya, create_group, import_exocortex_abc
from miraLibs.pipeLibs.pipeMaya import get_assets, get_valid_camera, set_frame_range_by_camera


def reference_in_camera(seq, shot, project):
    camera_publish_file = pipeFile.get_shot_step_camera_file(seq, shot, "anim", project)
    if not os.path.isfile(camera_publish_file):
        print "No camera abc found from anim."
        return
    create_reference.create_reference(camera_publish_file)
    print "reference in camera done."


def reference_in_anim_env(seq, shot, project):
    anim_env_publish_file = pipeFile.get_shot_step_env_file(seq, shot, "anim", project)
    if os.path.isfile(anim_env_publish_file):
        create_reference.create_reference(anim_env_publish_file)
        print "Reference in anim env publish file: %s" % anim_env_publish_file
    else:
        print "no env publish from anim." % anim_env_publish_file


def reference_in_anim_render(seq, shot, project):
    anim_render_publish_file = pipeFile.get_shot_step_anim_render_file(seq, shot, project)
    if os.path.isfile(anim_render_publish_file):
        create_reference.create_reference(anim_render_publish_file)
        print "Reference in anim env publish file: %s" % anim_render_publish_file
    else:
        print "no env publish from anim." % anim_render_publish_file


def reference_in_shd(seq, shot, project):
    asset_info_path = pipeFile.get_shot_step_assetinfo_file(seq, shot, "anim", project)
    if not os.path.isfile(asset_info_path):
        print "No asset info found, maybe no character or prop."
        return
    asset_info = yml_operation.get_yaml_data(asset_info_path)
    for asset_type in asset_info:
        assets = asset_info[asset_type]
        for asset in assets:
            name = assets[asset]["name"]
            namespace = assets[asset]["namespace"]
            type_long_name = assets[asset]["type"]
            shd_file = pipeFile.get_asset_step_publish_file(type_long_name, name, "shd", project)
            if not os.path.isfile(shd_file):
                print "%s is not an exist file." % shd_file
                continue
            create_reference.create_reference(shd_file, namespace, True)
    print "reference char and prop files done."


def get_caches(seq, shot, context, project, ext=".abc"):
    caches = list()
    cache_dir = pipeFile.get_shot_step_dir(seq, shot, context, "_cache", project)
    if not os.path.isdir(cache_dir):
        print "no .abc cache export from %s." % context
        return caches
    latest_cache_version = get_latest_version_dir.get_latest_version_dir(cache_dir)
    if not latest_cache_version:
        print "no %s latest cache found." % context
        return caches
    caches = get_children_file.get_children_file(latest_cache_version, ext)
    return caches


def attach(seq, shot, project):
    caches = get_caches(seq, shot, "anim", project)
    if not caches:
        print "No cache file(*.abc) found from anim"
        return
    print "attaching..."
    for cache in caches:
        try:
            import_exocortex_abc.import_exocortex_abc(cache)
        except:
            print "Can't attach %s." % cache
    print "attach done."


def reference_in_vfx_cache(seq, shot, project):
    sim_caches = get_caches(seq, shot, "sim", project)
    vfx_caches = get_caches(seq, shot, "vfx", project)
    caches = sim_caches + vfx_caches
    if not caches:
        print "No caches found from sim and vfx."
        return
    for cache in caches:
        create_reference.create_reference(cache)
    print "reference in vfx caches done."


def group_camera(file_path):
    camera = get_valid_camera.get_valid_camera(file_path)
    if camera:
        create_group.create_group("camera")
        mc.parent(camera, "camera")
    print "group camera done."


def group_assets():
    char_assets = get_assets.get_assets("char")
    if char_assets:
        create_group.create_group("char")
        mc.parent(char_assets, "char")
    prop_assets = get_assets.get_assets("prop")
    if prop_assets:
        create_group.create_group("prop")
        mc.parent(prop_assets, "prop")
    print "group assets done."


def main():
    logger = logging.getLogger("lgt start")
    file_path = options.file
    obj = pipeFile.PathDetails.parse_path(file_path)
    project = obj.project
    seq = obj.seq
    shot = obj.shot
    # rename to lgt start file
    mc.file(rename=file_path)
    load_plugin.load_plugin("AbcImport.mll")
    load_plugin.load_plugin("MayaExocortexAlembic.mll")
    # reference in camera
    reference_in_camera(seq, shot, project)
    # reference in char and prop shd file.
    reference_in_shd(seq, shot, project)
    # attach
    attach(seq, shot, project)
    # reference in anim published env
    reference_in_anim_env(seq, shot, project)
    # reference in anim render
    reference_in_anim_render(seq, shot, project)
    # reference in sim and vfx cache.
    reference_in_vfx_cache(seq, shot, project)
    # -group camera
    group_camera(file_path)
    # group assets
    group_assets()
    # set frame range
    set_frame_range_by_camera.set_frame_range_by_camera("cam_%s_%s" % (seq, shot))
    save_file.save_file()
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
