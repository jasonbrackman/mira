# -*- coding: utf-8 -*-
import maya.cmds as mc


def open_file(file_name, lnr=False):
    mc.file(file_name, open=1, f=1, loadNoReferences=lnr)


if __name__ == "__main__":
    pass
