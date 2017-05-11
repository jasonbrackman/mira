# -*- coding: utf-8 -*-
import pymel.core as pm
from miraLibs.pipeLibs.pipeMaya import get_asset_names, assign_uv


def assign_uv_back():
    assets = get_asset_names.get_asset_names()
    # delete all history
    pm.delete(assets, constructionHistory=1)
    for asset in assets:
        assign_uv.assign_uv(asset)


if __name__ == "__main__":
    assign_uv_back()
