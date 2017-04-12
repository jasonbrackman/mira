# -*- coding: utf-8 -*-
import re
import maya.cmds as mc


def sort_key(text):
    str_num = "".join(re.findall(r"\d", text))
    return str_num.zfill(10)


def add_namespace(namespace_name, model_group=None):
    mc.namespace(set=":")
    namespace_name = mc.namespace(add=namespace_name)
    if model_group and mc.objExists(model_group):
        children = mc.listRelatives(model_group, allDescendents=1)
        children.append(model_group)
        for child in children:
            mc.rename(child, "%s:%s" % (namespace_name, child))
