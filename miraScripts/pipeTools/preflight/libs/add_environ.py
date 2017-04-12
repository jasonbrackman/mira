# -*- coding: utf-8 -*-
import sys
import os
from PathGetter import PathGetter
import get_engine
from get_configuration_env_dir import get_configuration_env_dir


def insert_to_sys_path(sys_dir):
    if sys_dir not in sys.path:
        sys.path.insert(0, sys_dir)


def add_preflight_environ():
    preflight_package_dir = PathGetter.parse_path().package_dir
    insert_to_sys_path(preflight_package_dir)


def add_check_options_environ():
    check_options_engine_dir = PathGetter.parse_path().check_options_engine_dir
    insert_to_sys_path(check_options_engine_dir)


def add_configuration_environ():
    configuration_env_dir = get_configuration_env_dir()
    engine = get_engine.get_engine()
    check_options_engine_dir = os.path.join(configuration_env_dir, "check_options", engine)
    insert_to_sys_path(check_options_engine_dir)


def add_environ():
    add_preflight_environ()
    add_check_options_environ()
    add_configuration_environ()


if __name__ == "__main__":
    add_environ()
