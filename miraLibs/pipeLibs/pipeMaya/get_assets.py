# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_assets(asset_type):
    assets = list()
    transforms = mc.ls(type="transform")
    for transform in transforms:
        if transform.endswith("_MODEL"):
            transform_name = transform.split(":")[-1]
            if transform_name.startswith(asset_type+"_"):
                assets.append(transform)
    return assets
