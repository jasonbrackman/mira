# -*- coding: utf-8 -*-
import os
from miraLibs.pyLibs import yml_operation


class ConfParser(object):

    def __init__(self, path=None):
        self.path = path

    def get_conf_path(self):
        conf_dir = os.path.join(os.path.dirname(self.path), "conf")
        conf_path = os.path.join(conf_dir, "conf.yml")
        conf_path = conf_path.replace("\\", "/")
        return conf_path

    @property
    def conf_data(self):
        conf_path = self.get_conf_path()
        conf_data = yml_operation.get_yaml_data(conf_path)
        return conf_data
