__author__ = 'heshuai'

import maya.mel as mel


def build_new_scene_UI():
    mel.eval("deleteUI unifiedRenderGlobalsWindow;")
    mel.eval("buildNewSceneUI;")