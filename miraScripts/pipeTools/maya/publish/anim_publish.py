# -*- coding: utf-8 -*-
import optparse
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import export_model_abc, export_anim_env, \
    export_camera_abc, export_anim_asset_info
from miraLibs.mayaLibs import quit_maya, save_as, open_file, ReferenceUtility, \
    load_plugin, export_selected, delete_layer


def export_render_group(anim_render_path):
    if not mc.objExists("render"):
        return
    if not mc.listRelatives("render", children=1):
        return
    mc.select("render", r=1)
    export_selected.export_selected(anim_render_path, pr_flag=True)


def main():
    logger = logging.getLogger("anim publish")
    file_path = options.file
    open_file.open_file(file_path)
    # get path
    obj = pipeFile.PathDetails.parse_path(file_path)
    seq = obj.seq
    shot = obj.shot
    env_path = obj.env_path
    publish_path = obj.publish_path
    camera_path = obj.camera_path
    anim_render_path = obj.anim_render_path
    asset_info_path = obj.asset_info_path
    ru = ReferenceUtility.ReferenceUtility()
    # save to publish path
    delete_layer.delete_layer()
    save_as.save_as(publish_path)
    logger.info("Save to publish path: %s" % publish_path)
    # export shd env for light context.
    export_anim_env.export_anim_env(env_path)
    # export render group
    export_render_group(anim_render_path)
    # import all reference
    ru.import_loaded_ref()
    if mc.objExists("env"):
        mc.delete("env")
    if mc.objExists("render"):
        mc.delete("render")
    # export camera abc
    logger.info("start export camera cache...")
    export_camera_abc.export_camera_abc(seq, shot, camera_path, "frame_range")
    logger.info("start export asset information.")
    export_anim_asset_info.export_anim_asset_info(asset_info_path)
    # export prop char abc for light.
    logger.info("start export cache...")
    mc.file(rename=file_path)
    load_plugin.load_plugin("MayaExocortexAlembic.mll")
    export_model_abc.export_model_abc()
    # quit maya
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
