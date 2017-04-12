# -*- coding: utf-8 -*-
import get_latest_version


def get_new_version(file_path):
    return get_latest_version.get_latest_version(file_path, offset=1)
