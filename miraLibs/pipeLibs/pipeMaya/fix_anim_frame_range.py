# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import set_frame_range


def fix_anim_frame_range(seq, shot):
    shot_name = "shot_%s_%s" % (seq, shot)
    if not mc.objExists(shot_name):
        raise RuntimeError("%s is not exist." % shot_name)
    start_frame = mc.getAttr("%s.startFrame" % shot_name)
    end_frame = mc.getAttr("%s.endFrame" % shot_name)
    set_frame_range.set_frame_range(start_frame, end_frame)
    return True
