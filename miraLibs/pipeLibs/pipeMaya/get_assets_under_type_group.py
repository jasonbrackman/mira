# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_assets_under_type_group(asset_type="char"):
    type_assets = list()
    if mc.objExists(asset_type):
        assets = mc.listRelatives(asset_type, ad=1, type="transform")
        if assets:
            type_assets = [asset for asset in assets if asset.endswith("_MODEL")]
    return type_assets
