# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as mc


def get_all_meshes(mode="pymel"):
    if mode == "pymel":
        all_meshes = pm.ls(type="mesh")
    elif mode == "cmds":
        all_meshes = mc.ls(type="mesh")
    return all_meshes


if __name__ == "__main__":
    pass
