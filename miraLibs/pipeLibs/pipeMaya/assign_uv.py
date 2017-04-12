# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.api.OpenMaya as om
from miraLibs.mayaLibs import is_reference, get_namespace
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import json_operation, get_latest_version_by_dir


ASSET_DICT = {"char": "character", "prop": "prop", "env": "environment"}


def name_to_node(name):
    sList = om.MSelectionList()
    sList.add(name)
    node = sList.getDagPath(0)
    return node


def assign_uv_by_json_data(json_data):
    for mesh_name in json_data:
        mesh_node = name_to_node(mesh_name)
        mesh = om.MFnMesh(mesh_node)
        mesh.clearUVs()
        U_array = json_data[mesh_name]["U_array"]
        V_array = json_data[mesh_name]["V_array"]
        uv_counts = json_data[mesh_name]["uv_counts"]
        uvIds = json_data[mesh_name]["uvIds"]
        mesh.setUVs(U_array, V_array)
        mesh.assignUVs(uv_counts, uvIds)


def assign_uv(asset):
    """
    assign uv by json configuration
    :param asset: pymel short asset name
    :return:
    """
    scene_name = pm.sceneName()
    project_name = pipeFile.name_conversion(scene_name)[0]
    # get json path and data
    asset_short_name = asset.name()
    # below split(":") maybe some reference with namespace
    asset_type_simple = asset_short_name.split(":")[-1].split("_")[0]
    asset_type = ASSET_DICT[asset_type_simple]
    asset_name = asset_short_name.split(":")[-1].split("_")[1]
    # get json path and data
    json_dir = pipeFile.get_asset_dir(project_name, asset_type, asset_name, "shd", "uvjson")
    json_path = get_latest_version_by_dir.get_latest_version_by_dir(json_dir)
    json_data = json_operation.get_json_data(json_path[0])
    # assign uv
    asset_long_name = asset.longName()
    prefix = "|".join((asset_long_name.split("|")[:-1]))
    # -if not referenced
    if not is_reference.is_reference(asset):
        # -- has no prefix (just open the mdl file)
        if not prefix:
            assign_uv_by_json_data(json_data)
        # -- has prefix (has parent group)
        else:
            for mesh_name in json_data:
                final_mesh = prefix + mesh_name
                mesh_node = name_to_node(final_mesh)
                mesh = om.MFnMesh(mesh_node)
                mesh.clearUVs()
                U_array = json_data[mesh_name]["U_array"]
                V_array = json_data[mesh_name]["V_array"]
                uv_counts = json_data[mesh_name]["uv_counts"]
                uvIds = json_data[mesh_name]["uvIds"]
                mesh.setUVs(U_array, V_array)
                mesh.assignUVs(uv_counts, uvIds)
    # -referenced file
    else:
        namespace_name = get_namespace.get_namespace(asset_short_name)
        namespace_name = namespace_name.split(":", 1)[-1]
        # -- has no parent group
        if not prefix:
            # --- has no namespace (just reference in without namespace)
            if namespace_name == ":":
                assign_uv_by_json_data(json_data)
            # ---has namespace
            else:
                for mesh_name in json_data:
                    mesh_list = mesh_name.split("|")
                    final_mesh = ("|%s:" % namespace_name).join(mesh_list)
                    mesh_node = name_to_node(final_mesh)
                    mesh = om.MFnMesh(mesh_node)
                    mesh.clearUVs()
                    U_array = json_data[mesh_name]["U_array"]
                    V_array = json_data[mesh_name]["V_array"]
                    uv_counts = json_data[mesh_name]["uv_counts"]
                    uvIds = json_data[mesh_name]["uvIds"]
                    mesh.setUVs(U_array, V_array)
                    mesh.assignUVs(uv_counts, uvIds)
        # -- has parent group
        else:
            # has no namespace
            if namespace_name == ":":
                for mesh_name in json_data:
                    final_mesh = prefix + mesh_name
                    mesh_node = name_to_node(final_mesh)
                    mesh = om.MFnMesh(mesh_node)
                    mesh.clearUVs()
                    U_array = json_data[mesh_name]["U_array"]
                    V_array = json_data[mesh_name]["V_array"]
                    uv_counts = json_data[mesh_name]["uv_counts"]
                    uvIds = json_data[mesh_name]["uvIds"]
                    mesh.setUVs(U_array, V_array)
                    mesh.assignUVs(uv_counts, uvIds)
            # has namespace
            else:
                for mesh_name in json_data:
                    mesh_list = mesh_name.split("|")
                    final_mesh = ("|%s:" % namespace_name).join(mesh_list)
                    final_mesh = prefix + final_mesh
                    mesh_node = name_to_node(final_mesh)
                    mesh = om.MFnMesh(mesh_node)
                    mesh.clearUVs()
                    U_array = json_data[mesh_name]["U_array"]
                    V_array = json_data[mesh_name]["V_array"]
                    uv_counts = json_data[mesh_name]["uv_counts"]
                    uvIds = json_data[mesh_name]["uvIds"]
                    mesh.setUVs(U_array, V_array)
                    mesh.assignUVs(uv_counts, uvIds)


if __name__ == "__main__":
    pass
