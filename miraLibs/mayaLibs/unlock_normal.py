# -*- coding: utf-8 -*-
import maya.cmds as mc


def unlock_normal():
    mc.polyNormalPerVertex(ufn=1)
