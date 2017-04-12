# -*- coding: utf-8 -*-
import maya.cmds as mc


def rename_shape(prefix="", suffix="_GEOSHAPE"):
    selection = mc.ls(sl=1)
    if selection:
        all_shapes = mc.listRelatives(selection, ad=1, type="mesh")
    else:
        all_shapes = mc.ls(type="mesh")
    all_shape_parent = mc.listRelatives(all_shapes, p=1)
    all_shape_parent = list(set(all_shape_parent))
    for shape_parent in all_shape_parent:
        shape = mc.listRelatives(shape_parent, s=1, ni=1)[0]
        right_name = "%s%s%s" % (prefix, shape_parent, suffix)
        if shape == right_name:
            continue
        else:
            if mc.objExists(right_name):
                mc.rename(right_name, "%s_bak" % right_name)
            mc.rename(shape, right_name)
    return True
