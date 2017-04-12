# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import delete_models


def delete_extra_models(except_model):
    valid_transforms = ["persp", "top", "front", "side", except_model]
    invalid_transforms = list()
    transforms = mc.ls(assemblies=1)
    for transform in transforms:
        if transform not in valid_transforms:
            invalid_transforms.append(transform)
    if invalid_transforms:
        delete_models.delete_models(invalid_transforms)
