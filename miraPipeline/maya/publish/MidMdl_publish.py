# -*- coding: utf-8 -*-
import os
import logging
import optparse
import maya.cmds as mc
from miraLibs.pyLibs import copy
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import get_model_name
from miraLibs.mayaLibs import open_file, quit_maya, export_selected, delete_layer, \
    export_abc, new_file, Assembly, save_file

logger = logging.getLogger("MidMdl publish")


def main():
    file_path = options.file
    open_file.open_file(file_path)
    # get paths
    context = pipeFile.PathDetails.parse_path()
    copy_image_and_video(context)
    logger.info("copy image and video done.")
    export_to_publish(context)
    logger.info("export to publish done.")
    export_to_abc(context)
    logger.info("export to abc done")
    create_ad(context)
    logger.info("create ad done")
    # quit maya
    quit_maya.quit_maya()


def copy_image_and_video(context):
    # copy image and video to publish
    work_image_path = context.work_image_path
    work_video_path = context.work_video_path
    image_path = context.image_path
    video_path = context.video_path
    copy.copy(work_image_path, image_path)
    copy.copy(work_video_path, video_path)


def export_to_publish(context):
    # export _MODEL group to publish path
    publish_path = context.publish_path
    model_name = get_model_name.get_model_name()
    delete_layer.delete_layer()
    mc.select(model_name, r=1)
    export_selected.export_selected(publish_path)


def export_to_abc(context):
    # export abc
    model_name = get_model_name.get_model_name()
    logger.info(context.asset_type)
    if context.asset_type in ["Prop", "Character"]:
        logger.info("Exporting abc...")
        export_abc.export_abc(1, 1, context.abc_cache_path, model_name, False)
        logger.info("Exporting abc done")


def create_ad(context):
    if not os.path.isfile(context.abc_cache_path):
        logger.error("%s is not an exist file" % context.abc_cache_path)
        return
    ad_path = context.definition_path
    if os.path.isfile(ad_path):
        return
    new_file.new_file()
    mc.file(rename=ad_path)
    gpu_name = "%s_gpu" % context.step
    ad_node_name = "%s_%s_AD" % (context.asset_type_short_name, context.asset_name)
    assemb = Assembly.Assembly()
    node = assemb.create_assembly_node(ad_node_name, "assemblyDefinition")
    assemb.create_representation(node, "Cache", gpu_name, gpu_name, context.abc_cache_path)
    save_file.save_file()


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
