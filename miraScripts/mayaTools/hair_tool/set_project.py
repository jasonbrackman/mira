# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from miraLibs.mayaLibs import set_project


def main():
    scene_name = mc.file(q=1, sn=1)
    project_dir = os.path.dirname(scene_name)
    set_project.set_project(project_dir)
