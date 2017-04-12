# -*- coding: utf-8 -*-
import os


def create_parent_dir(path):
    parent_dir = os.path.dirname(path)
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir)
