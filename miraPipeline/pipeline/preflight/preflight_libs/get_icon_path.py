# -*- coding: utf-8 -*-
import os
from PathGetter import PathGetter


def get_icon_path(name):
    icon_dir = PathGetter.parse_path().icon_dir
    icon_path = os.path.join(icon_dir, "%s.png" % name)
    icon_path = icon_path.replace("\\", "/")
    return icon_path

