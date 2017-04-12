__author__ = 'heshuai'


import maya.cmds as mc


def set_layer_override(attr, value):
    mc.editRenderLayerAdjustment(attr)
    mc.setAttr(attr, value)