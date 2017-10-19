# -*- coding: utf-8 -*-
import os


def get_file_engine(filein):
    engine = None
    ext = os.path.splitext(filein)
    if ext in [".ma", ".mb"]:
        engine = "maya"
    elif ext in [".nk"]:
        engine = "nuke"
    elif ext in [".hip"]:
        engine = "houdini"
    return engine
