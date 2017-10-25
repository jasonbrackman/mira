# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
import maya.mel as mel
import save_file


def save_as(new_file_name):
    if new_file_name:
        if not os.path.isdir(os.path.dirname(new_file_name)):
            os.makedirs(os.path.dirname(new_file_name))
        mc.file(rename=new_file_name)
        save_file.save_file()
    else:
        mel.eval("SaveSceneAs;")


if __name__ == "__main__":
    pass
