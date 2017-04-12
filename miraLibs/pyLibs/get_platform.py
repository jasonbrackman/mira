# -*- coding: utf-8 -*-
import sys


def get_platform():
    if sys.platform.startswith("win"):
        platform = "windows"
    elif sys.platform.startswith("linux"):
        platform = "linux"
    else:
        platform = "osx"
    return platform
