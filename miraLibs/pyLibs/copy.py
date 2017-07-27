# -*- coding: utf-8 -*-
import os
import shutil


def copy(src, dst):
    dst_dir = os.path.dirname(dst)
    if (not src) or (not os.path.isfile(src)):
        print "%s is not an exist file" % src
        return
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    try:
        shutil.copyfile(src, dst)
        return True
    except:
        print "Can't copy %s--->%s" % (src, dst)
        return False
