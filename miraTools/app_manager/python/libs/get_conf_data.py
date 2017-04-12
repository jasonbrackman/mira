# -*- coding: utf-8 -*-
import os
from .conf_parser import ConfParser


def get_conf_dir():
    package_dir = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
    conf_dir = os.path.join(package_dir, "conf")
    conf_dir = conf_dir.replace("\\", "/")
    return conf_dir


def get_conf_data(conf_name):
    conf_dir = get_conf_dir()
    conf_path = os.path.join(conf_dir, conf_name)
    cp = ConfParser(conf_path)
    data = cp.parse().get()
    return data
