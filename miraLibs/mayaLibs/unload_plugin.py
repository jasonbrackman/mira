# -*- coding: utf-8 -*-
import maya.cmds as mc


def unload_plugin(plugin_name):
    if mc.pluginInfo(plugin_name, q=1, loaded=1):
        mc.unloadPlugin(plugin_name, f=1)
        mc.pluginInfo(plugin_name, e=1, autoload=0)


if __name__ == "__main__":
    pass
