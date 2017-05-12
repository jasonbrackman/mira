# -*- coding: utf-8 -*-
from miraLibs.pipeLibs.pipeDb import init_db_menu


def main():
    import maya.OpenMaya as OpenMaya
    OpenMaya.MEventMessage.addEventCallback("SceneOpened", init_db_menu.init_db_menu)
