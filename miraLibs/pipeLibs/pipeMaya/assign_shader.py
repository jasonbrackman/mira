# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
import pymel.core as pm
import miraLibs.pipeLibs.pipeFile as pipeFile
from miraLibs.pyLibs import json_operation, join_path
from miraLibs.mayaLibs import create_reference, get_namespace


ASSET_DICT = {"char": "character", "prop": "prop", "env": "environment"}
logger = logging.getLogger(__name__)


def exist_warning(value):
    logger.warning("Maya Node does not exist: %s" % value)


def assign_shader_by_json_data(json_data):
    not_exist_mdl_list = list()
    for mesh in json_data:
        sg_node = json_data[mesh]["sg"]
        is_mesh_exist = mc.objExists(mesh)
        is_sg_exist = mc.objExists(sg_node)
        if not is_mesh_exist:
            exist_warning(mesh)
            not_exist_mdl_list.append(mesh)
            continue
        if not is_sg_exist:
            exist_warning(sg_node)
            continue
        mc.sets(mesh, fe=json_data[mesh]["sg"])
        set_arnold_attribute(json_data, mesh, mesh)
    return not_exist_mdl_list


def set_arnold_attribute(json_data, mesh, final_mesh):
    try:
        pm.setAttr("%s.aiOpaque" % final_mesh, json_data[mesh]["opaque_attr"])
        mc.setAttr("%s.aiSubdivType" % final_mesh, json_data[mesh]["subdiv_type"])
        mc.setAttr("%s.aiSubdivIterations" % final_mesh, json_data[mesh]["subdiv_iterations"])
    except:
        return


def assign_shader(asset, shader_version):
    """
    assign shader by json configuration
    :param asset: pymel short asset name
    :param shader_version: default or other shader version
    :return:
    """
    not_exist_list = list()
    # get json path and data
    obj = pipeFile.PathDetails.parse_path()
    project = obj.project
    asset_short_name = asset.name()
    # below split(":") maybe some reference with namespace
    asset_type_simple = asset_short_name.split(":")[-1].split("_")[0]
    asset_type = ASSET_DICT[asset_type_simple]
    asset_name = asset_short_name.split(":")[-1].split("_")[1]
    json_dir = pipeFile.get_asset_step_dir(asset_type, asset_name, "shd", "_connection",
                                           project_name=project, shd_version=shader_version)
    json_path = join_path.join_path2(json_dir, "%s_%s_shd_v000.json" % (project, asset_name))
    if not json_path:
        logger.error("No connection json file found.")
        return
    json_data = json_operation.get_json_data(json_path)
    # get shd path and reference in
    shd_dir = pipeFile.get_asset_step_dir(asset_type, asset_name, "shd", "_sg",
                                          project_name=project, shd_version=shader_version)
    shd_path = join_path.join_path2(shd_dir, "%s_%s_shd_v000.mb" % (project, asset_name))
    if not shd_path:
        logger.error("No shading publish file found.")
        return
    # create reference
    create_reference.create_reference(shd_path)
    # assign shader
    asset_long_name = asset.longName()
    prefix = "|".join((asset_long_name.split("|")[:-1]))
    namespace_name = get_namespace.get_namespace(asset_short_name)
    namespace_name = namespace_name.strip(":")
    # has no parent group
    if not prefix:
        # -has no namespace
        if not namespace_name:
            not_exist = assign_shader_by_json_data(json_data)
            if not_exist:
                not_exist_list.extend(not_exist)
        # -has name space
        else:
            for mesh in json_data:
                mesh_list = mesh.split("|")
                final_mesh = ("|%s:" % namespace_name).join(mesh_list)
                if not mc.objExists(final_mesh):
                    exist_warning(final_mesh)
                    not_exist_list.append(final_mesh)
                    continue
                pm.sets(json_data[mesh]["sg"], fe=final_mesh)
                set_arnold_attribute(json_data, mesh, final_mesh)
    # has prefix (has parent group)
    else:
        # -has no namespace
        if not namespace_name:
            for mesh in json_data:
                final_mesh = prefix + mesh
                if not mc.objExists(final_mesh):
                    logger.warning("%s not exist." % final_mesh)
                    not_exist_list.append(final_mesh)
                    continue
                pm.sets(json_data[mesh]["sg"], fe=final_mesh)
                set_arnold_attribute(json_data, mesh, final_mesh)
        # -has namespace
        else:
            for mesh in json_data:
                mesh_list = mesh.split("|")
                final_mesh = ("|%s:" % namespace_name).join(mesh_list)
                final_mesh = prefix + final_mesh
                if not mc.objExists(final_mesh):
                    logger.warning("%s not exist." % final_mesh)
                    not_exist_list.append(final_mesh)
                    continue
                pm.sets(json_data[mesh]["sg"], fe=final_mesh)
                set_arnold_attribute(json_data, mesh, final_mesh)
    return not_exist_list


if __name__ == "__main__":
    pass
