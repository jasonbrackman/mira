#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/11/11
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
import maya.cmds as mc
# Studio modules

# Local modules


def delete_locked_node():
    selected_objects = mc.ls(sl=1)
    for selected_object in selected_objects:
        mc.lockNode(selected_object, lock=False)
        children = mc.listRelatives(selected_object, ad=1, f=1)
        if children:
            for child in mc.listRelatives(selected_object, ad=1, f=1):
                mc.lockNode(child, lock=False)


if __name__ == '__main__':
    delete_locked_node()