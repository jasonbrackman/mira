# -*- coding: utf-8 -*-
import maya.cmds as mc
from get_selected_group_sg import get_selected_group_sg


def get_selected_group_mat():
    sg_nodes = get_selected_group_sg()
    materials = list()
    for sg in sg_nodes:
        mat = mc.listConnections("%s.surfaceShader" % sg)
        if mat:
            materials.append(mat[0])
    return materials
