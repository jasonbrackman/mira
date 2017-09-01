# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pyLibs import json_operation


def export_shd_json_data(shd_json_path):
    """
    export json data like {mesh:{"shader":sg_node},.......}
    :return:
    """
    mdl_sg_dict = dict()
    normal_meshes = mc.ls(type="mesh", long=1, ni=1)
    yeti_meshes = mc.ls(type="pgYetiMaya", long=1)
    meshes = normal_meshes + yeti_meshes
    for mesh in meshes:
        sg_node = mc.listConnections(mesh, s=0, d=1, type="shadingEngine")
        subdiv_type = None
        subdiv_iterations = None
        opaque_attr = None
        if not sg_node:
            continue
        transform_node = mc.listRelatives(mesh, parent=1, fullPath=1)
        if len(transform_node) > 1:
            continue
        try:
            opaque_attr = mc.getAttr("%s.aiOpaque" % mesh)
            subdiv_type = mc.getAttr("%s.aiSubdivType" % mesh)
            subdiv_iterations = mc.getAttr("%s.aiSubdivIterations" % mesh)
        except:pass
        temp_dict = {"sg": sg_node[0],
                     "subdiv_type": subdiv_type,
                     "subdiv_iterations": subdiv_iterations,
                     "opaque_attr": opaque_attr}
        mdl_sg_dict[transform_node[0]] = temp_dict
    json_operation.set_json_data(shd_json_path, mdl_sg_dict)


if __name__ == "__main__":
    pass
