# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_models(indicate=None):
    if indicate:
        all_transforms = mc.listRelatives(indicate, ad=1, type="transform")
    else:
        all_transforms = mc.ls(type="transform")
    models = [i for i in all_transforms if i.endswith("_MODEL")]
    return models
