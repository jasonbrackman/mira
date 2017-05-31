# -*- coding: utf-8 -*-
import os
import yaml


def get_conf_path():
    conf_path = os.path.abspath(os.path.join(__file__, "..", "..", "..", "conf", "config.yml"))
    conf_path = conf_path.replace("\\", "/")
    return conf_path


def get_conf_data():
    conf_path = get_conf_path()
    with open(conf_path, "r") as f:
        data = yaml.load(f)
    return data
