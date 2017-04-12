# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_backup_group():
    backup_group = list()
    for trans in mc.ls(type="transform"):
        if trans.endswith("_BACKUP"):
            backup_group.append(trans)
    return backup_group
