# -*- coding: utf-8 -*-
import maya.cmds as mc


def remove_model_smooth():
    smooth_nodes = mc.ls(type="polySmoothFace")
    if not smooth_nodes:
        return
    for smooth_node in smooth_nodes:
        try:
            mc.setAttr("%s.divisions" % smooth_node, 0)
        except:pass


def main():
    remove_model_smooth()
