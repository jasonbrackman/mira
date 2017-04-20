#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_get_qss_path
# description : ''
# author      : HeShuai
# date        : 2016/1/18
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging

# Third-party modules

# Studio modules

# Local modules


def get_qss_path():
    current_path = __file__
    parent_dir = os.path.dirname(current_path)
    qss_path = os.path.abspath(os.path.join(parent_dir, 'style.qss'))
    return qss_path


if __name__ == "__main__":
    pass
