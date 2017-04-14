# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
import miraLibs.mayaLibs.offset_anim_keyframe as offset_anim_keyframe


def offset_keyframe(to_frame=1001, delete_shot=False):
    logger = logging.getLogger(__name__)
    # get offset
    shot = mc.ls(type="shot")
    if not len(shot) == 1:
        logger.error("Not one shot in the maya file")
        return
    start_frame = mc.getAttr("%s.sequenceStartFrame" % shot[0])
    frame_offset_value = to_frame-start_frame
    # offset all keyframes
    all_curves = mc.ls(type="animCurve")
    valid_curves = list()
    for curve in all_curves:
        is_ref = mc.referenceQuery(curve, inr=1)
        if not is_ref:
            valid_curves.append(curve)
    offset_anim_keyframe.offset_anim_keyframe(valid_curves, frame_offset_value)
    # delete shot
    if delete_shot:
        mc.delete(shot)
