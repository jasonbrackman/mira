# -*- coding: utf-8 -*-
import os
from . import get_platform


def start_file(exe_path):
    if not (os.path.isfile(exe_path) or os.path.isdir(exe_path)):
        return
    plat_form = get_platform.get_platform()
    if plat_form == "windows":
        os.startfile(exe_path)
    elif plat_form == "linux":
        os.system('xdg-open %s' % exe_path)
    else:
        pass
