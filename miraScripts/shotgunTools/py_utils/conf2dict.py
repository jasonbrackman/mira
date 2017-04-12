#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/11/30
# version     :
# usage       :
# notes       :

# Built-in modules
import ConfigParser
import os
# Third-party modules

# Studio modules

# Local modules


def conf2dict(conf_path):
    conf_path = conf_path.replace('\\', '/')
    if not os.path.isfile(conf_path):
        print "[AAS info]: source: %s      \n"  \
                           "\t\t\tcontent: %s is not an exist file" % (__file__, conf_path)
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
