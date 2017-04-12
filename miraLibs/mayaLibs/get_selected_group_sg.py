# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc


def get_selected_group_sg():
    sg_nodes = list()
    sel = mc.ls(sl=1)
    meshes = mc.listRelatives(sel, ad=1, type="mesh")
    if not meshes:
        return
    for mesh in meshes:
        sg_node = mc.listConnections(mesh, s=0, d=1, type="shadingEngine")
        if not sg_node:
            logging.warning("%s connect no shadingEngine" % mesh)
            continue
        sg_nodes.append(sg_node[0])
    sg_nodes = list(set(sg_nodes))
    return sg_nodes
