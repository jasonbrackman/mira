# -*- coding: utf-8 -*-
import maya.cmds as mc


def bake_frame(objects, start, end):
    mc.bakeResults(objects, simulation=1, t=(start, end), sampleBy=1, oversamplingRate=1,
                   disableImplicitControl=1, preserveOutsideKeys=1, sparseAnimCurveBake=0,
                   removeBakedAttributeFromLayer=0,
                   removeBakedAnimFromLayer=0, bakeOnOverrideLayer=0, minimizeRotation=1, controlPoints=0, shape=1)
