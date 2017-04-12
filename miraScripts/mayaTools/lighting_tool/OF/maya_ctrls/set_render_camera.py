__author__ = 'heshuai'


import maya.cmds as mc


def set_render_camera(camera):
    cameras = mc.ls(type='camera')
    for cam in cameras:
        mc.setAttr(cam+'.renderable', 0)
    mc.setAttr(camera+'.renderable', 1)