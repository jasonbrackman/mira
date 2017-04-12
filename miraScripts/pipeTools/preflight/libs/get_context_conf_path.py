# -*- coding: utf-8 -*-
import os
import get_engine
from get_configuration_env_dir import get_configuration_env_dir
from get_context import get_context
from PathGetter import PathGetter


def get_context_conf_path():
    context_conf_path = None
    engine = get_engine.get_engine()
    configuration_env_dir = get_configuration_env_dir()
    context = get_context()
    conf_file_name = "%s.yml" % context
    check_conf_file = os.path.join(configuration_env_dir, "check_conf", engine, conf_file_name)
    check_conf_file = check_conf_file.replace("\\", "/")
    if os.path.isfile(check_conf_file):
        context_conf_path = check_conf_file
    else:
        conf_dir = PathGetter.parse_path().check_conf_engine_dir
        check_conf_file = os.path.join(conf_dir, conf_file_name)
        check_conf_file = check_conf_file.replace("\\", "/")
        if os.path.isfile(check_conf_file):
            context_conf_path = check_conf_file
    return context_conf_path
