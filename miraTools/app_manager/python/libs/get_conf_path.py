# -*- coding: utf-8 -*-
import os
from . import get_conf_data
from . import get_platform


def get_app_conf_dir():
    app_conf_data = get_conf_data.get_conf_data("app_conf_dir.yml")
    platform = get_platform.get_platform()
    app_conf_dir = app_conf_data[platform]
    return app_conf_dir


def get_conf_path(conf_name):
    """
    get the conf path under the conf dir of configuration
    :param conf_name: conf file name
    :return:
    """
    app_conf_dir = get_app_conf_dir()
    recent_app_conf_path = os.path.join(app_conf_dir, conf_name)
    return recent_app_conf_path.replace("\\", "/")
