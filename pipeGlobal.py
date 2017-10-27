# -*- coding: utf-8 -*-
import os
from miraCore import *
from miraLibs.pipeLibs.Project import Project


class PipeGlobal(object):
    def __init__(self):
        self.__update()

    @staticmethod
    def __get_value(yml_name):
        from miraLibs.pyLibs import yml_operation
        yml_path = "%s/%s.yml" % (conf_dir, yml_name)
        return yml_operation.get_yaml_data(yml_path)

    def __company_value(self):
        return self.__get_value("company")

    @property
    def data(self):
        return self.__company_value()

    def __update(self):
        self.__dict__.update(self.data)


global_instance = PipeGlobal()
data = global_instance.data
company = global_instance.company
projects = global_instance.projects
current_project = global_instance.current_project
exe = global_instance.EXE


if __name__ == "__main__":
    print global_instance.data