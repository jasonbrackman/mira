# -*- coding: utf-8 -*-
import os
import get_package_dir
from miraLibs.pyLibs import yml_operation


def get_custom_dir():
    conf_dir = get_package_dir.conf_dir
    custom_config_path = "%s/custom.yml" % conf_dir
    conf_data = yml_operation.get_yaml_data(custom_config_path)
    cus_dir = conf_data.get("custom_dir")
    if not cus_dir or not os.path.isdir(cus_dir):
        cus_dir = get_package_dir.get_package_dir("miraCustom")
    cus_dir = cus_dir.replace("\\", "/")
    return cus_dir


custom_dir = get_custom_dir()
