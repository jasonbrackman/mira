# -*- coding: utf-8 -*-
import get_file_name
import get_engine


def get_context():
    try:
        from miraLibs.pipeLibs import pipeFile
        scene_name = get_file_name.get_file_name()
        x = pipeFile.PathDetails.parse_path(scene_name)
        return x.step
    except:
        engine = get_engine.get_engine()
        if engine == "maya":
            return "mdl"
        elif engine == "nuke":
            return "comp"
        elif engine == "houdini":
            return "vfx"
