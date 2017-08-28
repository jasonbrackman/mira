# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.mayaLibs import new_file, Assembly, save_file, rename_scene, export_abc


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


def export_cache(context):
    step = context.step
    if step == "AnimLay":
        switch_step = "MidRig"
    else:
        switch_step = "HighRig"
    # switch to rig
    assemb = Assembly.Assembly()
    assemb.set_active(switch_step)
    # export env cache
    cache_dir = context.cache_dir
    env_cache_path = "%s/env.abc" % cache_dir
    children = mc.listRelatives("Env", ad=1, type="transform")
    models = [child for child in children
              if child.endswith("_MODEL") and not child.split(":")[-1].startswith("env_")]
    export_abc.export_abc(1000, 1000, env_cache_path, models)
    # export other cache
