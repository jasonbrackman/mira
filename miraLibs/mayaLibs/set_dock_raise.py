# -*- coding: utf-8 -*-
import maya.cmds as mc


def set_dock_raise(dock_name):
    all_dock = mc.lsUI(type="dockControl")
    if not all_dock:
        return
    for dock in all_dock:
        dock_label = mc.dockControl(dock, q=1, l=1)
        if dock_label == dock_name:
            mc.dockControl(dock, e=1, r=1)
            break
