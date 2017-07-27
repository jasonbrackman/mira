# -*- coding: utf-8 -*-
import os
from distutils.dir_util import copy_tree


def copytree(src, dst):
    if not os.path.isdir(src):
        print "%s is not exist directory" % src
        return
    copy_tree(src, dst)


if __name__ == "__main__":
    pass