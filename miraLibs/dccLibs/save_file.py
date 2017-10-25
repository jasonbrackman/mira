# -*- coding: utf-8 -*-
import get_engine


def save_file():
    engine = get_engine.get_engine()
    if engine == "maya":
        from miraLibs.mayaLibs import save_file
    elif engine == "nuke":
        from miraLibs.nukeLibs import save_file
    else:
        return
    save_file.save_file()
