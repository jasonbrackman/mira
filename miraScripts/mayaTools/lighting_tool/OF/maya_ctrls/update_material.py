__author__ = 'heshuai'


import maya.cmds as mc


def update_material(status):
    mc.renderThumbnailUpdate(status)