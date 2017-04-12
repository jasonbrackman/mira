# -*- coding: utf-8 -*-
import os
import shutil


def remove_dir(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)
