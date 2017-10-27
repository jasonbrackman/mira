# -*- coding: utf-8 -*-
import os
import logging
import miraCore
import miraLibs.pyLibs.yml_operation as yml
import miraLibs.pyLibs.join_path as join_path


class Step(object):
    def __init__(self, project, step):
        self.__project = project
        self.__step = step
        self.__custom_dir = miraCore.custom_dir
        self.data = self.__get_value()
        self.__dict__.update(self.data)

    @property
    def conf_path(self):
        conf_path = join_path.join_path2(self.__custom_dir, self.__project, "step.yml")
        if not os.path.isfile(conf_path):
            conf_path = join_path.join_path2(self.__custom_dir, "defaultProject", "step.yml")
        return conf_path

    def __get_value(self):
        yml_data = yml.get_yaml_data(self.conf_path)
        if yml_data. has_key(self.__step):
            value = yml_data.get(self.__step)
            return value
        else:
            logging.error("Step KeyError: %s not in the config file" % self.__step)

    @property
    def conf_options(self):
        return self.data.keys()

    @property
    def entity(self):
        if self.entity_type == "Asset":
            return "asset"
        else:
            return "shot"


if __name__ == "__main__":
    print Step("s", "Anim").conf_options