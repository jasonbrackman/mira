#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """

import maya.cmds as mc
import get_maya_win


def show_ui(cls):
    instance = cls()
    if mc.window(str(instance.objectName()), q=1, ex=1):
        mc.deleteUI(str(instance.objectName()))
    ui = cls(get_maya_win.get_maya_win())
    print ui.objectName()
    ui.show()