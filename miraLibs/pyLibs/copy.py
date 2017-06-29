# -*- coding: utf-8 -*-
import os
import shutil


def copy(src, dst):
    dst_dir = os.path.dirname(dst)
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    if (not src) or (not os.path.isfile(src)):
        print "%s is not an exist file" % src
        return
    try:
        shutil.copy(src, dst)
        return True
    except:
        print "Can't copy %s--->%s" % (src, dst)
        return False
