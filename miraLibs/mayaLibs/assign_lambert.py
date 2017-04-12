# -*- coding: utf-8 -*-
import maya.cmds as mc


def assign_lambert():
    """
    export all the meshes without shader, for the rig publish
    :return:
    """
    all_meshes = mc.ls(type="mesh", long=1)
    default_sg = "initialShadingGroup"
    mc.sets(all_meshes, fe=default_sg)
