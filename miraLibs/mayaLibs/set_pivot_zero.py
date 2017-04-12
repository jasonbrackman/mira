# -*- coding: utf-8 -*-
import maya.cmds as mc


def set_all_pivot_zero():
    transforms = list(set(mc.ls(type='transform')) - set([u'persp', u'top', u'front', u'side']))
    set_transform_zero(transforms)


def set_transform_zero(transforms):
    for tr in transforms:
        mc.move(0, 0, 0, [tr+'.scalePivot', tr+'.rotatePivot'])
