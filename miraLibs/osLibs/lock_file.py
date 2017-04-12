# -*- coding: utf-8 -*-

import os


def lock_file(path):
    os.system(r"attrib +r %s" % path)
