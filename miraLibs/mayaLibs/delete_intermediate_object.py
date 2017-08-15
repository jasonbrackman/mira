# -*- coding: utf-8 -*-
import maya.cmds as mc


def delete_intermediate_object():
    intermediate_objects = mc.ls(type="mesh", io=1)
    if intermediate_objects:
        mc.delete(intermediate_objects)
