# -*- coding: utf-8 -*-
import os
import conf_parser
from PathGetter import PathGetter


def get_configuration_env_dir():
    pg = PathGetter.parse_path()
    configuration_dir = pg.configuration_dir
    conf_path = os.path.join(configuration_dir, "main.yml")
    cp = conf_parser.ConfParser(conf_path)
    conf_data = cp.parse().get()
    env_dir = conf_data["check_dir"]
    return env_dir


if __name__ == "__main__":
    print get_configuration_env_dir()