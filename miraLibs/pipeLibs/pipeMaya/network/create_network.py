# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.pyLibs import yml_operation, join_path


def create_network(**kwargs):
    # create network node
    if mc.objExists("ROOT"):
        return
    mc.createNode("network", name="ROOT")
    # add attributes
    conf_path = join_path.join_path2(os.path.dirname(__file__), "conf.yml")
    conf_data = yml_operation.get_yaml_data(conf_path)
    attributes_dict = conf_data["attributes"]
    for attr_type in attributes_dict:
        attributes = attributes_dict[attr_type].split(",")
        for attr in attributes:
            mc.addAttr("ROOT", ln=attr, dt=attr_type)
            mc.setAttr("ROOT.%s" % attr, e=1, keyable=1)
    # set attributes
    # -set custom attributes
    if kwargs:
        for attr in kwargs:
            if attr in attributes_dict["string"]:
                mc.setAttr("ROOT.%s" % attr, str(kwargs[attr]), type="string")
                mc.setAttr("ROOT.%s" % attr, l=1)
            else:
                logging.error("Attribute Error.")
    # lock the ROOT node
    mc.lockNode("ROOT", lock=1)
