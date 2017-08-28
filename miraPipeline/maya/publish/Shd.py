# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya, export_selected, \
    delete_history, delete_unused_nodes, delete_layer, \
    get_selected_group_sg, get_shader_history_nodes, remove_namespace, delete_intermediate_object
from miraLibs.pipeLibs.pipeMaya import rename_pipeline_shape, publish, get_model_name


def get_created_sg_node():
    exclude_sg = ["initialParticleSE", "initialShadingGroup"]
    sg_nodes = get_selected_group_sg.get_selected_group_sg()
    created_sg = list(set(sg_nodes)-set(exclude_sg))
    return created_sg


def get_prefix(context):
    asset_name = context.asset_name
    task = context.task
    prefix = asset_name+"_"+task+"_"
    return prefix


def rename_shd_mat_node(context):
    prefix = get_prefix(context)
    created_sg = get_created_sg_node()
    if not created_sg:
        return
    for sg in created_sg:
        material_nodes = get_shader_history_nodes.get_shader_history_nodes(sg)
        for node in material_nodes:
            if node.startswith(prefix):
                continue
            try:
                new_name = "%s%s" % (prefix, node)
                mc.rename(node, new_name)
            except:
                pass


def main(file_name, local):
    logger = logging.getLogger("shd publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    publish_path = context.publish_path
    # import all reference
    publish.reference_opt()
    logger.info("Import all reference.")
    # delete history and delete unused nodes
    delete_history.delete_history()
    delete_unused_nodes.delete_unused_nodes()
    # delete intermediate object
    delete_intermediate_object.delete_intermediate_object()
    logger.info("Delete intermediate_object done.")
    # remove namespace
    remove_namespace.remove_namespace()
    logger.info("Remove namespace done.")
    # rename mat node
    model_name = get_model_name.get_model_name()
    mc.select(model_name, r=1)
    rename_shd_mat_node(context)
    logger.info("Rename material name done.")
    # rename shape
    if not rename_pipeline_shape.rename_pipeline_shape():
        raise RuntimeError("Rename shape error.")
    logger.info("Rename shape done.")
    # export _MODEL to publish path
    delete_layer.delete_layer()
    export_selected.export_selected(publish_path)
    logger.info("Save to %s" % publish_path)
    # add to AD
    publish.add_mesh_to_ad(context)
    logger.info("Add to AD done.")
    if not local:
        quit_maya.quit_maya()
