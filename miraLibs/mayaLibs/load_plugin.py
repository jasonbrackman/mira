# -*- coding: utf-8 -*-
import maya.cmds as mc


def load_plugin(plugin_name, auto_load=True):
    if not mc.pluginInfo(plugin_name, q=1, loaded=1):
        mc.loadPlugin(plugin_name, quiet=1)
    if auto_load:
        mc.pluginInfo(plugin_name, edit=True, autoload=True)


if __name__ == "__main__":
    pass
