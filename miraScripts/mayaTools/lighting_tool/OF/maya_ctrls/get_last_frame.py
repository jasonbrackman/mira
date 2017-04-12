__author__ = 'heshuai'


import maya.cmds as mc


def get_last_frame():
    return mc.playbackOptions(max=1, q=1)