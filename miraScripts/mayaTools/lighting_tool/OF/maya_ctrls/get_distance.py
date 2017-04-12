#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """

import pymel.core as pm
import pymel.core.datatypes as dt
import maya.cmds as mc


def mix(a, b, r=0.5):
    return a + (b - a) * r


def get_pos(obj):
    if pm.PyNode(obj).type() == 'camera':
        obj_pos = pm.xform(obj, q=1, t=1, ws=1)
    else:
        obj_bb = mc.exactWorldBoundingBox(obj)
        obj_pos = [mix(obj_bb[0+x], obj_bb[3+x]) for x in range(3)]
    return obj_pos


def get_distance(obj1, obj2):
    obj1_pos = dt.Vector(get_pos(obj1))
    obj2_pos = dt.Vector(get_pos(obj2))
    return obj1_pos.distanceTo(obj2_pos)


