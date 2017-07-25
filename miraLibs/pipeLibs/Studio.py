# -*- coding: utf-8 -*-
import miraCore
import logging
import miraLibs.pyLibs.yml_operation as yml
import miraLibs.pyLibs.join_path as join_path


class Studio(object):
    def __init__(self, project):
        self.__project = project
        self.__conf_dir = miraCore.get_conf_dir()
        self.__value = self.value()

    def value(self):
        conf_path = join_path.join_path2(self.__conf_dir, "studio.yml")
        yml_data = yml.get_yaml_data(conf_path)
        if yml_data. has_key(self.__project):
            value = yml_data.get(self.__project)
            return value
        else:
            logging.error("Step: %s not in the config file: %s" % (self.__project, conf_path))
