#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """


import maya.cmds as mc


def load_plugin(plugin_name):
    if not mc.pluginInfo(plugin_name, q=1, loaded=1):
        mc.loadPlugin(plugin_name, quiet=1)