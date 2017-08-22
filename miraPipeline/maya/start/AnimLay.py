# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
from miraLibs.mayaLibs import new_file, save_as, create_group, quit_maya
from miraLibs.pipeLibs import pipeFile


def main(file_name, local):
    logger = logging.getLogger("AnimLay start")
    new_file.new_file()
    context = pipeFile.PathDetails.parse_path(file_name)
    project = context.project
    seq = context.seq
    shot = context.shot
    # create camera and create group
    camera_name = "cam_%s_%s" % (seq, shot)
    create_group.create_group("camera")
    cam = mc.camera()
    mc.rename(cam[1], "%sShape" % camera_name)
    camera = mc.rename(cam[0], camera_name)
    mc.parent(camera, "camera")
    # mc.lockNode(camera, l=1)
    create_group.create_group("env")
    create_group.create_group("char")
    create_group.create_group("prop")
    create_group.create_group("_REF")
    create_group.create_group("render")
    # set frame range
    mc.playbackOptions(e=1, minTime=101)
    mc.playbackOptions(e=1, maxTime=150)
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    if not local:
        quit_maya.quit_maya()
