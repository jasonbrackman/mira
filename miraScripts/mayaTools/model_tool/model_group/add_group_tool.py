#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur|http://wingedwhitetiger.com/'

import maya.cmds as cmds


def add_sel_to_group(grp_name, except_list):
    if not not len(cmds.ls(grp_name)):
        sel_list = [sel for sel in cmds.ls(sl=True) if sel not in except_list]
        if sel_list:
            cmds.parent(sel_list, grp_name)

