__author__ = 'heshuai'

import maya.cmds as mc


def set_persp_far():
    mc.setAttr('perspShape.farClipPlane',1000000)