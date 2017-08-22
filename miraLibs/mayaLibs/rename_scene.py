import os
import maya.cmds as mc


def rename_scene(file_name):
    file_dir = os.path.dirname(file_name)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    mc.file(rename=file_name)
