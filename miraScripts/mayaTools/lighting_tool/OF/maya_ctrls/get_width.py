__author__ = 'heshuai'


import maya.cmds as mc


def get_width():
    return mc.getAttr('defaultResolution.width')