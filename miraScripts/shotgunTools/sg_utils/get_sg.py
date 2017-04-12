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
import os
import sys
# Third-party modules

# Studio modules

# Local modules
from py_utils import conf2dict
from py_utils import get_conf_path


def get_sg_conf():
    conf_path = get_conf_path.get_conf_path()
    sg_conf_path = os.path.join(conf_path, 'sg.ini')
    return sg_conf_path


def get_sg(test=False):
    sg_conf = get_sg_conf()
    dict_of_conf = conf2dict.conf2dict(sg_conf)
    sg_script_path = dict_of_conf['shotgun_api3']['shotgun_api3_path']
    sys.path.insert(0, sg_script_path)
    import shotgun_api3 as shotgun
    if test:
        web_name = "http://shotgun-staging.antsanimation.com"
        script_name = 'hsToolkit'
        key = '2076a098b4e0e644762a2162a93cd6b6b9461ad102e1ac17b314089b032f4c79'
    else:
        web_name = "http://shotgun.antsanimation.com"
        script_name = 'aas_pipeline'
        key = 'e2154e4f8954899d2792cb80b7ae43fafc9051f96926a690dae394ffd9b59297'
    sg = shotgun.Shotgun(web_name, script_name, key)
    return sg
