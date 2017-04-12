# -*- coding: utf-8 -*-
import os


def get_icon_dir():
    icon_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons")
    icon_dir = icon_dir.replace("\\", "/")
    return icon_dir


if __name__ == "__main__":
    print get_icon_dir()
