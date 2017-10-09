# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.pyLibs import copy
from miraLibs.mayaLibs import delete_layer, export_selected, export_gpu_cache, new_file, Assembly, save_file, \
    open_file, import_load_remove_unload_ref
from miraLibs.pipeLibs.pipeMaya import get_model_name, rename_pipeline_shape


logger = logging.getLogger("miraLibs.pipeLibs.pipeMaya.asset_publish")


def copy_image_and_video(context):
    # copy image and video to publish
    work_image_path = context.work_image_path
    work_video_path = context.work_video_path
    image_path = context.image_path
    video_path = context.video_path
    copy.copy(work_image_path, image_path)
    copy.copy(work_video_path, video_path)


def export_need_to_publish(context, typ="model"):
    publish_path = context.publish_path
    model_name = get_model_name.get_model_name(typ=typ)
    delete_layer.delete_layer()
    mc.select(model_name, r=1)
    if context.step in ["MidRig", "HighRig"]:
        try:
            mc.select("Sets", add=1, ne=1)
        except:
            logger.info("No Sets group.")
    export_selected.export_selected(publish_path)


def reference_opt():
    import_load_remove_unload_ref.import_load_remove_unload_ref()


def rename_shape():
    return rename_pipeline_shape.rename_pipeline_shape()


def export_model_to_abc(context):
    # export gpu abc
    model_name = get_model_name.get_model_name()
    directory = os.path.dirname(context.abc_cache_path)
    filename = os.path.splitext(os.path.basename(context.abc_cache_path))[0]
    if context.asset_type in ["Prop", "Character", "Cprop", "Building"]:
        logger.info("Exporting abc...")
        export_gpu_cache.export_gpu_cache(model_name, directory, filename)
        logger.info("Exporting abc to %s" % context.abc_cache_path)


def create_ad(context):
    ad_path = context.definition_path
    if os.path.isfile(ad_path):
            return
    ad_node_name = "%s_%s_AD" % (context.asset_type_short_name, context.asset_name)
    if context.asset_type != "Environment":
        if not os.path.isfile(context.abc_cache_path):
            logger.error("%s is not an exist file" % context.abc_cache_path)
            return
        new_file.new_file()
        mc.file(rename=ad_path)
        gpu_name = "%s_gpu" % context.step
        assemb = Assembly.Assembly()
        node = assemb.create_assembly_node(ad_node_name, "assemblyDefinition")
        assemb.create_representation(node, "Cache", gpu_name, gpu_name, context.abc_cache_path)
        assemb.create_representation(node, "Scene", context.step, context.step, context.publish_path)
        save_file.save_file()
    else:
        new_file.new_file()
        mc.file(rename=ad_path)
        name = context.step
        assemb = Assembly.Assembly()
        node = assemb.create_assembly_node(ad_node_name, "assemblyDefinition")
        assemb.create_representation(node, "Scene", name, name, context.publish_path)
        save_file.save_file()


def add_high_mdl_ad(context):
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
    assemb.create_representation(ad_node_name, "Scene", context.step, context.step, context.publish_path)
    save_file.save_file()


def add_mesh_to_ad(context):
    if not os.path.isfile(context.publish_path):
        logger.error("%s is not an exist file." % context.publish_path)
        return
    ad_path = context.definition_path
    if not os.path.isfile(ad_path):
        logger.error("AD file not exist.")
        return
    try:
        open_file.open_file(ad_path)
    except:
        pass
    ad_node_name = "%s_%s_AD" % (context.asset_type_short_name, context.asset_name)
    print ad_node_name
    mesh_name = context.step
    assemb = Assembly.Assembly()
    assemb.create_representation(ad_node_name, "Scene", mesh_name, mesh_name, context.publish_path)
    save_file.save_file()


def export_material(context):
    from miraLibs.mayaLibs import get_selected_group_sg, export_selected
    sg_nodes = get_selected_group_sg.get_selected_group_sg()
    init_sg_nodes = ["initialParticleSE", "initialShadingGroup"]
    for sg_node in init_sg_nodes:
        if sg_node in sg_nodes:
            sg_nodes.remove(sg_node)
    if not sg_nodes:
        logger.info("No sg nodes found")
        return
    mc.select(sg_nodes, r=1, ne=1)
    shd_path = context.shd_path
    export_selected.export_selected(shd_path)


def export_connection(context):
    from miraLibs.pipeLibs.pipeMaya.shd import export_shd_json_data
    connection_path = context.connection_path
    export_shd_json_data.export_shd_json_data(connection_path)
