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
    # yeti_meshes = mc.ls(type="pgYetiMaya", long=1)
    yeti_meshes = []
    meshes = normal_meshes + yeti_meshes
    # below is arnold
    # for mesh in meshes:
    #     sg_node = mc.listConnections(mesh, s=0, d=1, type="shadingEngine")
    #     subdiv_type = None
    #     subdiv_iterations = None
    #     opaque_attr = None
    #     if not sg_node:
    #         continue
    #     transform_node = mc.listRelatives(mesh, parent=1, fullPath=1)
    #     if len(transform_node) > 1:
    #         continue
    #     try:
    #         opaque_attr = mc.getAttr("%s.aiOpaque" % mesh)
    #         subdiv_type = mc.getAttr("%s.aiSubdivType" % mesh)
    #         subdiv_iterations = mc.getAttr("%s.aiSubdivIterations" % mesh)
    #     except:pass
    #     temp_dict = {"sg": sg_node[0],
    #                  "subdiv_type": subdiv_type,
    #                  "subdiv_iterations": subdiv_iterations,
    #                  "opaque_attr": opaque_attr}
    for mesh in meshes:
        sg_node = mc.listConnections(mesh, s=0, d=1, type="shadingEngine")
        if not sg_node:
            continue
        transform_node = mc.listRelatives(mesh, parent=1, fullPath=1)
        if len(transform_node) > 1:
            continue
        rsEnableSubdivision = None
        rsSubdivisionRule = None
        rsScreenSpaceAdaptive = None
        rsDoSmoothSubdivision = None
        rsMinTessellationLength = None
        rsMaxTessellationSubdivs = None
        rsOutOfFrustumTessellationFactor = None
        rsEnableDisplacement = None
        rsMaxDisplacement = None
        rsDisplacementScale = None
        rsAutoBumpMap = None
        try:
            rsEnableSubdivision = mc.getAttr("%s.rsEnableSubdivision" % mesh)
            if rsEnableSubdivision:
                rsSubdivisionRule = mc.getAttr("%s.rsSubdivisionRule" % mesh)
                rsScreenSpaceAdaptive = mc.getAttr("%s.rsScreenSpaceAdaptive" % mesh)
                rsDoSmoothSubdivision = mc.getAttr("%s.rsDoSmoothSubdivision" % mesh)
                rsMinTessellationLength = mc.getAttr("%s.rsMinTessellationLength" % mesh)
                rsMaxTessellationSubdivs = mc.getAttr("%s.rsMaxTessellationSubdivs" % mesh)
                rsOutOfFrustumTessellationFactor = mc.getAttr("%s.rsOutOfFrustumTessellationFactor" % mesh)
            rsEnableDisplacement = mc.getAttr("%s.rsEnableDisplacement" % mesh)
            if rsEnableDisplacement:
                rsMaxDisplacement = mc.getAttr("%s.rsMaxDisplacement" % mesh)
                rsDisplacementScale = mc.getAttr("%s.rsDisplacementScale" % mesh)
                rsAutoBumpMap = mc.getAttr("%s.rsAutoBumpMap" % mesh)
        except:pass
        temp_dict = {"sg": sg_node[0],
                     "rsEnableSubdivision": rsEnableSubdivision,
                     "rsSubdivisionRule": rsSubdivisionRule,
                     "rsScreenSpaceAdaptive": rsScreenSpaceAdaptive,
                     "rsDoSmoothSubdivision": rsDoSmoothSubdivision,
                     "rsMinTessellationLength": rsMinTessellationLength,
                     "rsMaxTessellationSubdivs": rsMaxTessellationSubdivs,
                     "rsOutOfFrustumTessellationFactor": rsOutOfFrustumTessellationFactor,
                     "rsEnableDisplacement": rsEnableDisplacement,
                     "rsMaxDisplacement": rsMaxDisplacement,
                     "rsDisplacementScale": rsDisplacementScale,
                     "rsAutoBumpMap": rsAutoBumpMap}
        mdl_sg_dict[transform_node[0]] = temp_dict
    json_operation.set_json_data(shd_json_path, mdl_sg_dict)


if __name__ == "__main__":
    pass
