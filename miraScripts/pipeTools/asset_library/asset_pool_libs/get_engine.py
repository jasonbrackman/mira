# -*- coding: utf-8 -*-
import os
import sys


def get_engine():
    engine = None
    engine_path = sys.executable
    engine_base_name = os.path.basename(engine_path)
    if "maya" in engine_base_name:
        engine = "maya"
    elif "Nuke" in engine_base_name:
        engine = "nuke"
    elif "houdini" in engine_base_name:
        engine = "houdini"
    return engine
