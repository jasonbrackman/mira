__author__ = 'heshuai'


import maya.cmds as mc


def get_first_frame():
    return mc.playbackOptions(min=1, q=1)

