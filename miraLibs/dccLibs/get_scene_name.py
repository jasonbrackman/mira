# -*- coding: utf-8 -*-
import get_engine


def get_scene_name():
    file_name = None
    engine = get_engine.get_engine()
    if engine == "maya":
        import maya.cmds as mc
        file_name = mc.file(q=1, sn=1)
    elif engine == "nuke":
        import nuke
        file_name = nuke.root().name()
    elif engine == "houdini":
        import hou
        file_name = hou.hipFile().path()
    return file_name
