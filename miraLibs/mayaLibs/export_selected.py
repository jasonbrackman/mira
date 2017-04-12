# -*- coding: utf-8 -*-
import os
import pymel.core as pm


def export_selected(file_path, maya_type="mayaBinary", pr_flag=False):
    """
    :param file_path:
    :param maya_type:
    :param pr_flag: if True: export still as reference, else: import
    :return:
    """
    parent_dir = os.path.dirname(file_path)
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir)
    pm.exportSelected(file_path, type=maya_type, force=1, pr=pr_flag)


if __name__ == "__main__":
    pass
