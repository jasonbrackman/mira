# -*- coding: utf-8 -*-
import os
import miraCore
import logging
import miraLibs.pyLibs.yml_operation as yml
import miraLibs.pyLibs.join_path as join_path


class Studio(object):
    def __init__(self, project):
        self.__project = project
        self.__custom_dir = miraCore.custom_dir
        self.__value = self.value()

    def value(self):
        conf_path = join_path.join_path2(self.__custom_dir, self.__project, "studio.yml")
        if not os.path.isfile(conf_path):
            conf_path = join_path.join_path2(self.__custom_dir, "defaultProject", "studio.yml")
        if os.path.isfile(conf_path):
            dcp = yml.DeepConfParser(conf_path)
            yml_data = dcp.parse()
            return yml_data
        else:
            logging.error("Step: %s not in the config file: %s" % (self.__project, conf_path))
