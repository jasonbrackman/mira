# -*- coding: utf-8 -*-
import os
import maya.cmds as mc


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
    if file_path.endswith(".mb"):
        maya_type = maya_type
    elif file_path.endswith(".ma"):
        maya_type = "mayaAscii"
    mc.file(file_path, typ=maya_type, options="v=0", force=1, es=1, pr=pr_flag)


if __name__ == "__main__":
    pass
