# -*- coding: utf-8 -*-
import os
from miraLibs.pyLibs import get_next_version
from miraLibs.mayaLibs import save_as
from miraLibs.pyLibs import get_new_version_by_dir


def save_as_next_version_file(path, padding=3):
    next_version_file = get_next_version.get_next_version(path, padding)
    if os.path.isfile(next_version_file):
        new_version_file = get_new_version_by_dir.get_new_version_by_dir(os.path.dirname(next_version_file))
        next_version_file = new_version_file[0]
    save_as.save_as(next_version_file)
    return next_version_file
