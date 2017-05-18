# -*- coding: utf-8 -*-
import os
import shutil


def copy(src, dst):
    dst_dir = os.path.dirname(dst)
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    shutil.copy(src, dst)
