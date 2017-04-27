# -*- coding: utf-8 -*-
import os


def get_version_number(path, offset=0):
    base_name = os.path.basename(path)
    base_name_split_list = base_name.split("_")
    version_string = base_name_split_list[-1].split(".")[0]
    version_number = int(version_string[1:]) + offset
    return version_number
