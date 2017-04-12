# -*- coding: utf-8 -*-
import maya.cmds as mc


def add_string_attr(object_name, attr_long_name, default_value=None, locked=True):
    mc.addAttr(object_name, ln=attr_long_name, dt="string")
    mc.setAttr("%s.%s" % (object_name, attr_long_name), e=1, keyable=1)
    if default_value:
        mc.setAttr("%s.%s" % (object_name, attr_long_name), default_value, type="string")
    if locked:
        mc.setAttr("%s.%s" % (object_name, attr_long_name), l=1)

