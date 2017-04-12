# -*- coding: utf-8 -*-
from miraLibs.mayaLibs import get_all_meshes
from miraLibs.pyLibs import json_operation
import maya.api.OpenMaya as om


def name_to_node(name):
    sList = om.MSelectionList()
    sList.add(name)
    node = sList.getDagPath(0)
    return node


def get_uv_info():
    all_meshes = [mesh.longName() for mesh in get_all_meshes.get_all_meshes()]
    uv_dict = dict()
    for mesh_name in all_meshes:
        mesh_node = name_to_node(mesh_name)
        mesh = om.MFnMesh(mesh_node)

        U_array, V_array = mesh.getUVs()
        uv_counts, uvIds = mesh.getAssignedUVs()

        json_data = {"U_array": list(U_array),
                     "V_array": list(V_array),
                     "uv_counts": list(uv_counts),
                     "uvIds": list(uvIds)
                     }
        uv_dict[mesh_name] = json_data
    return uv_dict


def export_uv_json_data(json_path):
    json_data = get_uv_info()
    json_operation.set_json_data(json_path, json_data)


if __name__ == "__main__":
    pass
