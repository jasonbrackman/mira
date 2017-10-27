# -*- coding: utf-8 -*-
import os
import sys
import functools
import pymel.core as pm
from miraLibs.mayaLibs import maya_shelf_opt
from miraLibs.pyLibs import join_path, yml_operation
import pipeGlobal


def get_buttons():
    # get conf path
    conf_dir = pipeGlobal.conf_dir
    shelf_conf_path = join_path.join_path2(conf_dir, "maya_shelf.yml")
    shelf_conf_data = yml_operation.get_yaml_data(shelf_conf_path)
    pipeline_shelf = shelf_conf_data["pipeline_shelf"]
    pipeline_buttons = sorted(pipeline_shelf, key=lambda key: pipeline_shelf[key]["order"])
    return pipeline_buttons


def main():
    # delete shelf
    top_shelf = pm.melGlobals['gShelfTopLevel']
    # get buttons from yml
    pipeline_buttons = get_buttons()
    # create shelf
    maya_shelf_opt.delete_shelf(top_shelf, "PipeLine")
    maya_shelf_opt.create_shelf(top_shelf, "PipeLine")
    # get icon dir
    icon_dir = pipeGlobal.icons_dir
    shelf_icon_dir = join_path.join_path2(icon_dir, "maya_shelf_buttons")
    # create buttons
    sys.path.insert(0, os.path.dirname(__file__))
    for button in pipeline_buttons:
        cmd_text = "import {0}; reload({0}); {0}.main()".format(button)
        btn_command = functools.partial(exec_cmd, cmd_text)
        icon_path = join_path.join_path2(shelf_icon_dir, "%s.png" % button)
        maya_shelf_opt.create_shelf_button(button, "PipeLine", btn_command, icon_path)


def exec_cmd(cmd):
    exec(cmd)


if __name__ == "__main__":
    main()
