# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile


def set_render_dir():
    context = pipeFile.PathDetails.parse_path()
    render_dir = context.as_template("render")
    mc.workspace(fileRule=["images", render_dir])


def open_render_dir():
    context = pipeFile.PathDetails.parse_path()
    render_dir = context.as_template("render")
    if os.path.isdir(render_dir):
        os.startfile(render_dir)
    else:
        logging.error("%s is not an exist dir." % render_dir)
