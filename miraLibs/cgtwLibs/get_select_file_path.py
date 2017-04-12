## -*- coding: utf-8 -*-
import sys
sys.path.append("C:/Program Files/cgteamwork")
from cgtw import *


def get_select_file_path():
    """

    :return: selected files in cgtw, type: list
    """
    t_tw = tw("app_key123")
    t_file = t_tw.sys().get_sys_file()
    return t_file
