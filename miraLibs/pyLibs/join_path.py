# -*- coding: utf-8 -*-
import os


def join_path(*args):
    path = os.path.abspath(os.path.join(*args))
    return path


def join_path2(*args):
    path = join_path(*args)
    path = path.replace("\\", "/")
    return path


if __name__ == "__main__":
    pass
