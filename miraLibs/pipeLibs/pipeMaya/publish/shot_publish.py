# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.mayaLibs import new_file, Assembly, save_file, rename_scene, export_abc, get_frame_range, get_namespace
from miraLibs.pipeLibs.pipeMaya import get_models, get_valid_camera


logger = logging.getLogger("miraLibs.pipeLibs.pipeMaya.shot_publish")


def create_shot_ad(context):
    ad_path = context.definition_path
    if os.path.isfile(ad_path):
        return
    ad_node_name = "%s_%s_AD" % (context.sequence, context.shot)
    if not os.path.isfile(context.publish_path):
        logger.error("%s is not an exist file" % context.publish_path)
        return
    new_file.new_file()
    rename_scene.rename_scene(ad_path)
    assemb = Assembly.Assembly()
    name = context.step
    node = assemb.create_assembly_node(ad_node_name, "assemblyDefinition")
    assemb.create_representation(node, "Scene", name, name, context.publish_path)
    save_file.save_file()

# #####################################export cache#####################################


def export_cache(context):
    step = context.step
    if step == "AnimLay":
        switch_step = "MidRig"
    else:
        switch_step = "HighRig"
    # switch to rig
    assemb = Assembly.Assembly()
    assemb.set_active(switch_step)
    logger.info("Set assembly active done")
    # export camera cache
    export_camera_cache(context)
    logger.info("Export camera cache done.")
    # export env cache
    export_env_cache(context)
    logger.info("Export env cache done.")
    # export other cache
    export_other_cache(context, "Prop")
    logger.info("Export Prop cache done.")
    export_other_cache(context, "Char")
    logger.info("Export Char cache done.")


def export_camera_cache(context):
    valid_camera = get_valid_camera.get_valid_camera()
    if not mc.objExists(valid_camera):
        logger.error("No valid camera: %s exist." % valid_camera)
    cache_dir = context.cache_dir
    start, end = get_frame_range.get_frame_range()
    camera_cache_path = "%s/camera.abc" % cache_dir
    export_abc.export_abc(start, end, camera_cache_path, valid_camera)


def export_env_cache(context):
    cache_dir = context.cache_dir
    env_cache_path = "%s/env.abc" % cache_dir
    children = mc.listRelatives("Env", ad=1, type="transform")
    models = [child for child in children
              if child.endswith("_MODEL") and not child.split(":")[-1].startswith("env_")]
    export_abc.export_abc(1000, 1000, env_cache_path, models)


def export_other_cache(context, category):
    """
    export cprop prop and character cache
    :param context:
    :param category: Prop or Character
    :return:
    """
    if not mc.objExists(category):
        return
    cache_dir = context.cache_dir
    start, end = get_frame_range.get_frame_range()
    if context.step == "AnimLay":
        if category == "Prop":
            models = get_models.get_models("Prop")
        else:
            children = mc.listRelatives("Char", ad=1, type="transform")
            models = [i for i in children if i.endswith("DeformationSystem")]
        for model in models:
            namespace = get_namespace.get_namespace(model)
            cache_path = "%s/%s.abc" % (cache_dir, namespace)
            export_abc.export_abc(start, end, cache_path, model, False)


# #####################################export asset info#####################################


def export_asset_info():
    pass
