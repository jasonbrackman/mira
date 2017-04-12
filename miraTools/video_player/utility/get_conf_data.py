# -*- coding: utf-8 -*-
import yml_operation
import os


conf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yml")


def get_conf_data():
    yml_data = yml_operation.get_yaml_data(conf_path)
    return yml_data


def get_ffmpeg_path():
    conf_data = get_conf_data()
    ffmpeg_path = conf_data["ffmpeg_path"]
    return ffmpeg_path


def get_valid_ext():
    conf_data = get_conf_data()
    ext_data = conf_data["valid_ext"]
    ext_list = ext_data.split(",")
    return ext_list
