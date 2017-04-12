#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/12/22
# version     :
# usage       :
# notes       :

# Built-in modules
import os
# Third-party modules

# Studio modules

# Local modules
from conf2dict import conf2dict
from get_conf_path import get_conf_path


def get_conf_data():
    conf_path = get_conf_path()
    conf_file_path = os.path.join(conf_path, 'sg.ini')
    conf_data = conf2dict(conf_file_path)
    return conf_data
