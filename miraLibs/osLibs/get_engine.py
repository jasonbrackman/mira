# -*- coding: utf-8 -*-
import os
import sys


def get_engine():
    app = sys.executable
    app_basename = os.path.basename(app)
    app_name = os.path.splitext(app_basename)[0]
    if "Nuke" in app_name:
        app_name = "nuke"
    elif "houdini" in app_name:
        app_name = "houdini"
    elif "Photoshop" in app_name:
        app_name = "photoshop"
    elif "maya" in app_name:
        app_name = "maya"
    return app_name


if __name__ == "__main__":
    print get_engine()