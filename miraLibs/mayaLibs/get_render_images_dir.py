# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_render_images_dir():
    images_dir = mc.workspace(fileRuleEntry="images")
    if images_dir == "images":
        images_dir = mc.workspace(expandName="images")
    return images_dir
