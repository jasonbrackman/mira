# -*- coding: utf-8 -*-
import os
import get_engine
from PathGetter import PathGetter
from get_configuration_env_dir import get_configuration_env_dir


def get_check_py_file(module_name):
    py_file = None
    file_base_name = "%s.py" % module_name
    env_dir = get_configuration_env_dir()
    engine = get_engine.get_engine()
    if env_dir:
        check_options_file = os.path.join(env_dir, "check_options", engine, file_base_name)
        check_options_file = check_options_file.replace("\\", "/")
        if os.path.isfile(check_options_file):
            py_file = check_options_file
    if not py_file:
        check_options_engine_dir = PathGetter.parse_path().check_options_engine_dir
        check_options_file = os.path.join(check_options_engine_dir, file_base_name)
        check_options_file = check_options_file.replace("\\", "/")
        if os.path.isfile(check_options_file):
            py_file = check_options_file
    return py_file
