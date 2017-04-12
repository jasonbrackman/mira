# -*- coding: utf-8 -*-
import os
import re


def get_next_version(path, padding=3):
    base_name = os.path.basename(path)
    base_name_split_list = base_name.split("_")
    version_string = base_name_split_list[-1].split(".")[0]
    current_version = int(version_string[1:])
    next_version = current_version + 1
    next_version_file = re.sub("_v\d{%s}\." % padding, "_v%s." % str(next_version).zfill(3), path)
    next_version_file = next_version_file.replace("\\", "/")
    return next_version_file
