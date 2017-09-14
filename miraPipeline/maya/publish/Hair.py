# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import get_model_name, publish
from miraLibs.mayaLibs import open_file, quit_maya, export_abc, Xgen, export_selected
from miraLibs.pyLibs import json_operation


def main(file_name, local):
    logger = logging.getLogger("Hair publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    hair_cache_path = context.abc_cache_path
    hair_path = context.hair_path
    delta_path = context.delta_path
    asset_name = context.asset_name
    # import reference
    publish.reference_opt()
    # copy image
    publish.copy_image_and_video(context)
    logger.info("Copy image done.")
    # export SCULP group to abc
    model_name = get_model_name.get_model_name("hair")
    export_abc.export_abc(1, 1, hair_cache_path, model_name)
    logger.info("Export abc done.")
    # export xgen file
    collection_node = str("%s_collection" % asset_name)
    xgen = Xgen.Xgen()
    xgen.export_palette(collection_node, hair_path)
    xgen.create_delta(collection_node, delta_path)
    logger.info("Export .xgen file done.")
    # export shd
    export_shd(context)
    logger.info("Export shader done.")
    if not local:
        quit_maya.quit_maya()


def get_descriptions():
    import xgenm as xgen
    collections = xgen.palettes()
    needed_collection = collections[0]
    descriptions = xgen.descriptions(needed_collection)
    return descriptions


def get_all_hair_sg_nodes():
    hair_sg_nodes = list()
    connection_dict = dict()
    descriptions = get_descriptions()
    if not descriptions:
        return
    for description in descriptions:
        shapes = mc.listRelatives(description, s=1)
        if not shapes:
            continue
        shape = shapes[0]
        sg_nodes = mc.listConnections(shape, s=0, d=1, type="shadingEngine")
        if not sg_nodes:
            continue
        sg_node = sg_nodes[0]
        hair_sg_nodes.append(sg_node)
        connection_dict[description] = sg_node
    return hair_sg_nodes, connection_dict


def export_shd(context):
    sg_nodes, connection_dict = get_all_hair_sg_nodes()
    if not sg_nodes:
        return
    mc.select(sg_nodes, r=1, ne=1)
    export_selected.export_selected(context.shd_path)
    json_operation.set_json_data(context.connection_path, connection_dict)
