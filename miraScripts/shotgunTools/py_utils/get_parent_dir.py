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


current_path = __file__


def get_parent_dir(path=current_path):
    if os.path.isdir(path):
        path = os.path.abspath(path)
    elif os.path.isfile(path):
        path = os.path.dirname(path)
    parent_path = os.path.dirname(path)
    return parent_path
