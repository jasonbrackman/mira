# -*- coding: utf-8 -*-
import get_engine


def get_scene_name():
    engine = get_engine.get_engine()
    if engine == "maya":
        import maya.cmds as mc
        scene_name = mc.file(q=1, sn=1)
    elif engine == "nuke":
        import nuke
        scene_name = nuke.root().name()
    else:
        scene_name = None
    return scene_name