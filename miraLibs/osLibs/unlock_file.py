# -*- coding: utf-8 -*-
import os


def unlock_file(path):
    os.system(r"attrib -r %s" % path)
