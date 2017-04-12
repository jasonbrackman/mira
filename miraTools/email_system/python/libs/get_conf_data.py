# -*- coding: utf-8 -*-
import os
from . import yml_operation


def get_conf_dir():
    python_package_dir = os.path.dirname(os.path.dirname(__file__))
    conf_dir = os.path.join(os.path.dirname(python_package_dir), "conf")
    return conf_dir


def get_conf_data(conf_name):
    conf_dir = get_conf_dir()
    conf_path = os.path.join(conf_dir, "%s.yml" % conf_name)
    conf_data = yml_operation.get_yaml_data(conf_path)
    return conf_data
