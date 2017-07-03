# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.pyLibs import copy
from miraLibs.mayaLibs import delete_layer, export_selected, export_abc, new_file, Assembly, save_file, open_file
from miraLibs.pipeLibs.pipeMaya import get_model_name

logger = logging.getLogger("miraLibs.pipeLibs.pipeMaya.asset_publish")


def copy_image_and_video(context):
    # copy image and video to publish
    work_image_path = context.work_image_path
    work_video_path = context.work_video_path
    image_path = context.image_path
    video_path = context.video_path
    copy.copy(work_image_path, image_path)
    copy.copy(work_video_path, video_path)


def export_need_to_publish(context):
    # export _MODEL group to publish path
    publish_path = context.publish_path
    model_name = get_model_name.get_model_name()
    delete_layer.delete_layer()
    mc.select(model_name, r=1)
    export_selected.export_selected(publish_path)


def export_model_to_abc(context):
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


def add_gpu_to_ad(context):
    if not os.path.isfile(context.abc_cache_path):
        logger.error("%s is not an exist file" % context.abc_cache_path)
        return
    ad_path = context.definition_path
    if not os.path.isfile(ad_path):
        logger.error("AD file not exist.")
        return
    open_file.open_file(ad_path)
    ad_node_name = "%s_%s_AD" % (context.asset_type_short_name, context.asset_name)
    gpu_name = "%s_gpu" % context.step
    assemb = Assembly.Assembly()
    assemb.create_representation(ad_node_name, "Cache", gpu_name, gpu_name, context.abc_cache_path)
