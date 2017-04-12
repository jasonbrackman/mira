# -*- coding: utf-8 -*-
import ConfigParser
import os


def conf2dict(conf_path):
    conf_path = conf_path.replace('\\', '/')
    if not os.path.isfile(conf_path):
        return
    conf = ConfigParser.ConfigParser()
    conf.read(conf_path)
    dict_of_conf = dict()
    sections = conf.sections()
    for section in sections:
        kvs = conf.items(section)
        temp_dict = dict()
        for kv in kvs:
            temp_dict[kv[0]] = kv[1]
        dict_of_conf[section] = temp_dict
    return dict_of_conf

