# -*- coding: utf-8 -*-
import os
from deep_conf_parser import DeepConfParser


def get_conf_dir():
    conf_dir = os.path.abspath(os.path.join(__file__, "..", "..", "conf"))
    conf_dir = conf_dir.replace("\\", "/")
    return conf_dir


def get_templates_path():
    conf_dir = get_conf_dir()
    templates_path = os.path.join(conf_dir, "templates.yml").replace("\\", "/")
    return templates_path


def get_conf_data():
    templates_path = get_templates_path()
    dcp = DeepConfParser(templates_path)
    return dcp.parse()


if __name__ == "__main__":
    print get_conf_data()


