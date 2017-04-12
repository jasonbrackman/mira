# -*- coding: utf-8 -*-
import sys
sys.path.append("C:/Program Files/cgteamwork")
from cgtw import *


def get_shot_linked_assets(project, seq, shot):
    T_tw = tw('')
    T_project = T_tw.project()
    # get project name
    T_project.init_with_project_code(project)
    # get database name
    T_database = T_project.get_project_database()[0]['project_tab.data_base']
    T_shot = T_tw.shot(T_database)
    T_asset = T_tw.asset(T_database)

    T_shot.init_with_filter([["eps_tab.eps_name", "=", seq]])
    shots = T_shot.get(["shot_info_tab.shot", "shot_info_tab.asset_id"])

    asset_list = list()
    for each_shot in shots:
        shot_name = each_shot["shot_info_tab.shot"]
        if shot_name != shot:
            continue
        asset_ids = each_shot["shot_info_tab.asset_id"]
        asset_ids = asset_ids.split(",")
        T_asset.init_with_id(asset_ids)
        assets = T_asset.get(["asset_info_tab.asset_name", "asset_conf_type.name"])
        if not assets:
            return
        asset_list = list()
        for asset in assets:
            asset_type = asset["asset_conf_type.name"]
            asset_name = asset["asset_info_tab.asset_name"]
            asset_list.append([asset_type, asset_name])
    return asset_list
