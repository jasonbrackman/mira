# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
from miraLibs.mayaLibs import set_frame_range


def set_frame_range_by_camera(camera):
    logger = logging.getLogger(__name__)
    if not mc.objExists(camera):
        logger.error("camera not found.")
        return
    if mc.ls("%s.frame_range" % camera):
        frame_range_str = mc.getAttr("%s.frame_range" % camera)
        start_frame, end_frame = [int(value) for value in frame_range_str.split("-")]
        set_frame_range.set_frame_range(start_frame, end_frame)
    else:
        logger.warning("%s has no attribute frame_range" % camera)
