# -*- coding: utf-8 -*-
import maya.cmds as mc
import get_all_hair_file_node


def get_all_hair_textures():
    textures = list()
    file_nodes = get_all_hair_file_node.get_all_hair_file_node()
    if file_nodes:
        textures = [mc.getAttr("%s.fileTextureName" % file_node).replace("\\", "/") for file_node in file_nodes]
    return textures
