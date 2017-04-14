# -*- coding: utf-8 -*-
import os


def get_icon(arg):
    icon_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "icons"))
    if arg:
        icon_path = os.path.normpath(os.path.join(icon_dir, "green_bullet.png"))
    else:
        icon_path = os.path.normpath(os.path.join(icon_dir, "red_bullet.png"))
    icon_path = icon_path.replace("\\", "/")
    return icon_path
