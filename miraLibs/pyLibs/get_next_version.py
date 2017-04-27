# -*- coding: utf-8 -*-
import re
import get_version_number


def get_next_version(path, padding=3):
    next_version = get_version_number.get_version_number(path, 1)
    next_version_file = re.sub("_v\d{%s}\." % padding, "_v%s." % str(next_version).zfill(3), path)
    next_version_file = next_version_file.replace("\\", "/")
    return next_version_file
