__author__ = 'heshuai'



import maya.cmds as mc


def get_height():
    return mc.getAttr('defaultResolution.height')