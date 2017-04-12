# -*- coding: utf-8 -*-
import os


def get_icon_dir():
    package_dir = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
    icon_dir = os.path.join(package_dir, "icons")
    icon_dir = icon_dir.replace("\\", "/")
    return icon_dir


def get_icon_path(name):
    icon_dir = get_icon_dir()
    icon_path = os.path.join(icon_dir, name)
    icon_path = icon_path.replace("\\", "/")
    return icon_path


if __name__ == "__main__":
    print get_icon_path("sgdesk")
