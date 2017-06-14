# -*- coding: utf-8 -*-
import maya.cmds as mc
import pymel.core as pm


def get_selected_group_sg():
    sg_nodes = list()
    sel = mc.ls(sl=1)
    meshes = mc.listRelatives(sel, ad=1, type="mesh")
    if not meshes:
        return
    for mesh in meshes:
        sg_node = mc.listConnections(mesh, s=0, d=1, type="shadingEngine")
        if not sg_node:
            continue
        sg_nodes.append(sg_node[0])
    sg_nodes = list(set(sg_nodes))
    return sg_nodes


def get_shader_history_nodes(node, include_self=True, include_type=["file"]):
    if not pm.objExists(node):
        print "%s is not an exist node"
        return
    if isinstance(node, basestring):
        node = pm.PyNode(node)
    history_node = list()

    def get_history_node(node):
        input_nodes = list(set(node.inputs()))
        if not input_nodes:
            return
        for input_node in input_nodes:
            if input_node.type() in include_type:
                history_node.append(input_node.name())
            get_history_node(input_node)
    get_history_node(node)
    if include_self:
        history_node.append(node.name())
    history_node = list(set(history_node))
    return history_node


def maya_get_file_nodes():
    sg_nodes = get_selected_group_sg()
    if not sg_nodes:
        return
    file_nodes = list()
    for sg_node in sg_nodes:
        file_node = get_shader_history_nodes(sg_node, False)
        if file_node:
            file_nodes.extend(file_node)
    return list(set(file_nodes))
