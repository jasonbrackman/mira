# -*- coding: utf-8 -*-
import get_engine


def save_as(file_name=None):
    engine = get_engine.get_engine()
    if engine == "maya":
        from miraLibs.mayaLibs import save_as
    elif engine == "nuke":
        from miraLibs.nukeLibs import save_as
    else:
        return
    save_as.save_as(file_name)
