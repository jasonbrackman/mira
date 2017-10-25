# -*- coding: utf-8 -*-
import os
import nuke


def save_as(path, overwrite=1):
    if path:
        file_dir = os.path.dirname(path)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        nuke.scriptSaveAs(path, overwrite=overwrite)
    else:
        nuke.scriptSaveAs()
