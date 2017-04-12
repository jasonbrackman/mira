# -*- coding: utf-8 -*-
import os
import re


def get_file_version(path):
    path = path.replace("\\", "/")
    basename = os.path.basename(path)
    basename = os.path.splitext(basename)[0]
    pattern = ".*_v(\d+)$"
    matched_list = re.findall(pattern, basename)
    version = int(matched_list[-1]) if matched_list else None
    return version
