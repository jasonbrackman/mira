# -*- coding: utf-8 -*-
import os
import maya.cmds as mc


def get_file_texture_name(file_node):
    texture = mc.getAttr("%s.fileTextureName" % file_node)
    if not os.path.splitdrive(texture)[0]:
        texture = "%s%s" % (mc.workspace(q=1, rootDirectory=1, fullName=1), texture)
    return texture

