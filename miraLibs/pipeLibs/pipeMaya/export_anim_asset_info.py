# -*- coding: utf-8 -*-
from miraLibs.pyLibs import yml_operation
from miraLibs.mayaLibs import get_namespace
from miraLibs.pipeLibs.pipeMaya import get_assets_under_type_group


ASSET_DICT = {"char": "character", "prop": "prop"}


def export_anim_asset_info(path):
    asset_info_dict = dict()
    char_dict = get_asset_type_dict("char")
    if char_dict:
        asset_info_dict["char"] = char_dict
    prop_dict = get_asset_type_dict("prop")
    if prop_dict:
        asset_info_dict["prop"] = prop_dict
    yml_operation.set_yaml_path(path, asset_info_dict)


def get_asset_type_dict(asset_type):
    asset_dict = dict()
    assets = get_assets_under_type_group.get_assets_under_type_group(asset_type)
    if not assets:
        return
    for index, asset in enumerate(assets):
        asset_key = "%s%s" % (asset_type, index)
        temp_dict = dict()
        model_name = asset.split(":")[-1]
        name = model_name.split("_")[1]
        namespace = get_namespace.get_namespace(asset)
        temp_dict["name"] = str(name)
        temp_dict["namespace"] = str(namespace)
        temp_dict["type"] = str(ASSET_DICT[asset_type])
        asset_dict[asset_key] = temp_dict
    return asset_dict
