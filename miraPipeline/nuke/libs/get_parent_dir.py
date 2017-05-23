# -*- coding: utf-8 -*-
import os


current_path = __file__


def get_parent_dir(path=current_path):
    if os.path.isdir(path):
        path = os.path.abspath(path)
    elif os.path.isfile(path):
        path = os.path.dirname(path)
    parent_path = os.path.dirname(path)
    return parent_path
