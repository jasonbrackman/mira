# -*- coding: utf-8 -*-
import os
import logging
from miraLibs.mayaLibs import get_scene_name


def main():
    scene_name = get_scene_name.get_scene_name()
    cwd = os.path.dirname(scene_name)
    if cwd:
        os.startfile(cwd)
    else:
        logging.warning("No file opened.")
