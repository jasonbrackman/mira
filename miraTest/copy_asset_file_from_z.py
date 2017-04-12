# -*- coding: utf-8 -*-
import os
import shutil
from miraLibs.pyLibs import get_latest_version_by_dir, join_path

tar_dir = r"Q:\tianhuo\Shotgun\projects\df\_library\assets"
src_dir = r"Z:\Shotgun\projects\df\_library\assets"

asset_types = ["Character", "Environment", "Prop"]

for asset_type in asset_types:
    asset_type_folder = join_path.join_path2(tar_dir, asset_type)
    for asset_name in os.listdir(asset_type_folder):
        asset_rig_folder = join_path.join_path2(asset_type_folder, asset_name, "rig")
        if os.path.isdir(asset_rig_folder):
            shutil.rmtree(asset_rig_folder)
            print "remove %s" % asset_rig_folder
        asset_rig_publish_folder = join_path.join_path2(asset_rig_folder, "_publish")

        src_asset_rig_folder = join_path.join_path2(src_dir, asset_type, asset_name, "rig")
        if not os.path.isdir(src_asset_rig_folder):
            continue
        src_asset_rig_publish_folder = join_path.join_path2(src_asset_rig_folder, "_publish")

        latest_version_info = get_latest_version_by_dir.get_latest_version_by_dir(src_asset_rig_publish_folder)
        if not latest_version_info:
            continue
        latest_version = latest_version_info[0]
        base_name = os.path.basename(latest_version)
        tar_asset_rig_publish_file = join_path.join_path2(asset_rig_publish_folder, base_name)
        os.makedirs(asset_rig_publish_folder)
        try:
            shutil.copy(latest_version, tar_asset_rig_publish_file)
            print "copy %s to %s" % (latest_version, tar_asset_rig_publish_file)
        except Exception as e:
            print e


if __name__ == "__main__":
    pass
