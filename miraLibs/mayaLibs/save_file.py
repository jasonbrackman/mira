# -*- coding: utf-8 -*-
import maya.cmds as mc


def save_file():
    scene_name = mc.file(q=1, sn=1)
    if scene_name.endswith(".mb"):
        mc.file(save=1, f=1, type="mayaBinary")
    elif scene_name.endswith(".ma"):
        mc.file(save=1, f=1, type="mayaAscii")


if __name__ == "__main__":
    pass
