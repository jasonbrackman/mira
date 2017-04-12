# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
import create_network
from miraLibs.pyLibs import join_path, yml_operation


def change_network(**kwargs):
    create_network.create_network()
    conf_path = join_path.join_path2(os.path.dirname(__file__), "conf.yml")
    conf_data = yml_operation.get_yaml_data(conf_path)
    attributes_dict = conf_data["attributes"]
    mc.lockNode("ROOT", lock=0)
    for attr in kwargs:
        if attr in attributes_dict["string"]:
            mc.setAttr("ROOT.%s" % attr, l=0)
            mc.setAttr("ROOT.%s" % attr, kwargs[attr], type="string")
            mc.setAttr("ROOT.%s" % attr, l=1)
    mc.lockNode("ROOT", lock=1)
