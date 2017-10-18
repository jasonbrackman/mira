# -*- coding: utf-8 -*-
from miraLibs.pyLibs import json_operation
from miraLibs.mayaLibs import get_namespace
from miraLibs.pipeLibs.pipeMaya import get_assets_under_type_group


ASSET_DICT = {"char": "Character", "prop": "Prop", "cprop": "CProp"}


def export_anim_asset_info(path):
    char_asset_list = get_asset_type_list("Char")
    prop_asset_list = get_asset_type_list("Prop")
    asset_info_list = char_asset_list + prop_asset_list
    if asset_info_list:
        json_operation.set_json_data(path, asset_info_list)
    else:
        print "No asset found"


def get_asset_type_list(group):
    asset_info_list = list()
    assets = get_assets_under_type_group.get_assets_under_type_group(group)
    if assets:
        for asset in assets:
            temp_dict = dict()
            model_name = asset.split(":")[-1]
            name = model_name.split("_")[1]
            asset_type_short_name = model_name.split("_")[0]
            asset_type = ASSET_DICT.get(asset_type_short_name)
            namespace = get_namespace.get_namespace(asset)
            temp_dict["name"] = str(name)
            temp_dict["namespace"] = str(namespace)
            temp_dict["type"] = str(asset_type)
            asset_info_list.append(temp_dict)
    return asset_info_list


if __name__ == "__main__":
    export_anim_asset_info("D:/test.json")
