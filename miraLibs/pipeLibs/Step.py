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
        self.__value = self.value()

    def value(self):
        conf_path = join_path.join_path2(self.__custom_dir, self.__project, "step.yml")
        if not os.path.isfile(conf_path):
            conf_path = join_path.join_path2(self.__custom_dir, "defaultProject", "step.yml")
        yml_data = yml.get_yaml_data(conf_path)
        if yml_data. has_key(self.__step):
            value = yml_data.get(self.__step)
            return value
        else:
            logging.error("Step KeyError: %s not in the config file" % self.__step)

    @property
    def engine(self):
        return self.__value.get("engine")

    @property
    def up_step(self):
        return self.__value.get("up_step")

    @property
    def down_step(self):
        return self.__value.get("down_step")

    @property
    def entity_type(self):
        return self.__value.get("entity")

    @property
    def entity(self):
        if self.entity_type == "Asset":
            return "asset"
        else:
            return "shot"


if __name__ == "__main__":
    print repr(Step("SnowKidTest", "AnimLay").down_step)