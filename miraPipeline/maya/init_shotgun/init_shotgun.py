# -*- coding: utf-8 -*-
from miraLibs.pipeLibs.pipeSg import init_shotgun_menu


def main():
    import maya.OpenMaya as OpenMaya
    OpenMaya.MEventMessage.addEventCallback("SceneOpened", init_shotgun_menu.init_shotgun_menu)
