# -*- coding: utf-8 -*-
import logging
from Qt.QtWidgets import *
import maya.cmds as mc
import pymel.core as pm
import miraLibs.pipeLibs.pipeFile as pipeFile
from miraLibs.pyLibs import json_operation
from miraLibs.mayaLibs import create_reference, get_namespace
from miraLibs.mayaLibs import get_maya_globals


ASSET_DICT = {"char": "Character", "prop": "Prop", "cprop": "Cprop", "env": "Environment", "build": "Building"}
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
        set_renderer_attribute(json_data, mesh, mesh)
    return not_exist_mdl_list


def set_renderer_attribute(json_data, mesh, final_mesh):
    attrs = ["rsEnableSubdivision", "rsSubdivisionRule", "rsScreenSpaceAdaptive", "rsDoSmoothSubdivision",
             "rsMinTessellationLength", "rsMaxTessellationSubdivs", "rsOutOfFrustumTessellationFactor",
             "rsEnableDisplacement", "rsMaxDisplacement", "rsDisplacementScale", "rsAutoBumpMap"]
    for attr in attrs:
        try:
            attr_value = json_data.get(mesh).get(attr)
            if attr_value is not None:
                mc.setAttr("%s.%s" % (final_mesh, attr), json_data.get(mesh).get(attr))
        except:
            pass


def reference_shd(shd_path):
    shd_path = shd_path.replace("\\", "/")
    reference_files = mc.file(q=1, r=1, wcn=1)
    if shd_path in reference_files:
        return  
    create_reference.create_reference(shd_path)


def assign_shader(asset):
    """
    assign shader by json configuration
    :param asset: pymel short asset name
    :param shader_version: default or other shader version
    :return:
    """
    not_exist_list = list()
    # below split(":") maybe some reference with namespace
    asset_type_simple = asset.split(":")[-1].split("_")[0]
    asset_type = ASSET_DICT[asset_type_simple]
    asset_name = asset.split(":")[-1].split("_")[1]
    maya_globals = get_maya_globals.get_maya_globals()
    project = maya_globals.get("currentProject").project
    json_path = pipeFile.get_task_file(project, asset_type, asset_name, "Shd", "Shd", "maya_asset_connection", "")
    if not json_path:
        logger.error("No connection json file found.")
        return
    json_data = json_operation.get_json_data(json_path)
    # get shd path and reference in
    shd_path = pipeFile.get_task_file(project, asset_type, asset_name, "Shd", "Shd", "maya_asset_shd", "")
    if not shd_path:
        logger.error("No shading publish file found.")
        return
    # create reference
    reference_shd(shd_path)
    # assign shader
    asset_long_name = mc.ls(asset, long=1)[0]
    prefix = "|".join((asset_long_name.split("|")[:-1]))
    namespace_name = get_namespace.get_namespace(asset)
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
                set_renderer_attribute(json_data, mesh, final_mesh)
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
                set_renderer_attribute(json_data, mesh, final_mesh)
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
                set_renderer_attribute(json_data, mesh, final_mesh)
    return not_exist_list


def main():
    asset = mc.ls(sl=1)
    if len(asset) == 1 and asset[0].endswith("_MODEL"):
        assign_shader(asset[0])
        QMessageBox.information(None, "Warming Tip", "Assign shader done.")
    else:
        logger.error("Select right group.")
        QMessageBox.critical(None, "Warming Tip", "Select right group please.")


if __name__ == "__main__":
    main()
