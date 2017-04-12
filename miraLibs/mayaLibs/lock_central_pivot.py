# -*- coding: utf-8 -*-
import maya.cmds as mc


def lock_central_pivot(node):
    mc.setAttr("%s.rotatePivot" % node, lock=1)
    mc.setAttr("%s.scalePivot" % node, lock=1)
