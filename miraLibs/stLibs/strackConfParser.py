# -*- coding: utf-8 -*-
import os
from miraLibs.pyLibs import yml_operation


class StrackConfParser(object):

    def __init__(self):
        pass

    @staticmethod
    def get_conf_path():
        conf_dir = os.path.join(os.path.dirname(__file__), "strack_conf")
        conf_path = os.path.join(conf_dir, "strack.yml")
        conf_path = conf_path.replace("\\", "/")
        return conf_path

    @classmethod
    def st_conf_data(cls):
        obj = cls()
        conf_path = obj.get_conf_path()
        conf_data = yml_operation.get_yaml_data(conf_path)
        return conf_data
