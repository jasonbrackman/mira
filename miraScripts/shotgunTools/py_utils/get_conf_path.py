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
# Third-party modules

# Studio modules

# Local modules
import get_parent_dir


def get_conf_path():
    parent_dir = get_parent_dir.get_parent_dir()
    conf_path = os.path.join(parent_dir, 'conf')
    conf_path = conf_path.replace('\\', '/')
    return conf_path
