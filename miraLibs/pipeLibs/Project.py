# -*- coding: utf-8 -*-
import os
import miraCore
import logging
import miraLibs.pyLibs.yml_operation as yml
import miraLibs.pyLibs.join_path as join_path
from miraLibs.pipeLibs import Step


class Project(object):
    def __init__(self, project):
        self.__project = project
        self.__custom_dir = miraCore.custom_dir
        self.data = self.__value()
        self.__dict__.update(self.data)

    def __get_conf_path(self, yml_name):
        conf_path = join_path.join_path2(self.__custom_dir, self.__project, "%s.yml" % yml_name)
        if not os.path.isfile(conf_path):
            conf_path = join_path.join_path2(self.__custom_dir, "defaultProject", "%s.yml" % yml_name)
        return conf_path

    @property
    def conf_path(self):
        return self.__get_conf_path("project")

    @property
    def template_path(self):
        return self.__get_conf_path("template")

    def __get_value(self, yml_path):
        if os.path.isfile(yml_path):
            dcp = yml.DeepConfParser(yml_path)
            yml_data = dcp.parse()
            return yml_data
        else:
            logging.error("%s is not a config file." % self.conf_path)

    def __value(self):
        project_data = self.__get_value(self.conf_path)
        return project_data

    def get(self, key):
        if key in self.data:
            return self.data.get(key)

    @property
    def template_data(self):
        return self.__get_value(self.template_path)

    @property
    def templates(self):
        return self.template_data.keys()

    def template(self, template_str):
        return self.template_data.get(template_str)

    def step(self, step_value):
        return Step(self.__project, step_value)

    @property
    def conf_options(self):
        return self.data.keys()


if __name__ == "__main__":
    print Project("s").resolution
