# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_scene_name():
    scene_name = mc.file(q=1, sn=1)
    return scene_name
