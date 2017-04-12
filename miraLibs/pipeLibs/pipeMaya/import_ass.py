# -*- coding: utf-8 -*-
import os
import glob
import maya.cmds as mc
from miraLibs.mayaLibs import create_group, load_plugin


def import_my_ass(ass_path):
    load_plugin.load_plugin("mtoa.mll")
    base_name = os.path.basename(ass_path)
    base_name = base_name.strip("@")
    name_list = base_name.split("@")
    for index, i in enumerate(name_list[:-1]):
        parent = "standin" if index == 0 else name_list[index-1]
        create_group.create_group(i, parent)
    ass_shape_name = os.path.splitext(name_list[-1])[0]
    ass_shape = mc.createNode("aiStandIn", name=ass_shape_name, parent=name_list[-2])
    mc.setAttr("%s.dso" % ass_shape, ass_path, type="string")


def import_ass(ass_dir):
    ass_files = glob.glob("%s/*.ass" % ass_dir)
    if not ass_files:
        return
    for ass_file in ass_files:
        import_my_ass(ass_file)
