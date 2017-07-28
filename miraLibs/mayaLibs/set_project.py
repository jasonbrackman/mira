# -*- coding: utf-8 -*-
import maya.mel as mel


def set_project(project_dir):
    mel.eval('setProject \"' + project_dir + '\"')
