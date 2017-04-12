# -*- coding: utf-8 -*-

import sys


def get_os_type():
    """
    Return the type of current operation system like "windows" "osx" or "Linux"
    :return os_type: string
    """

    if sys.platform.startswith("win"):
        os_type = "windows"
    elif sys.platform.startswith("linux"):
        os_type = "linux"
    else:
        os_type = "osx"
    return os_type
