# -*- coding: utf-8 -*-
import os
import sys


def get_platform():
    if sys.platform.startswith("win"):
        platform = "windows"
    elif sys.platform.startswith("linux"):
        platform = "linux"
    else:
        platform = "osx"
    return platform


def start_file(exe_path):
    if not (os.path.isfile(exe_path) or os.path.isdir(exe_path)):
        return
    plat_form = get_platform()
    if plat_form == "windows":
        os.startfile(exe_path)
    elif plat_form == "linux":
        os.system('xdg-open %s' % exe_path)
    else:
        pass