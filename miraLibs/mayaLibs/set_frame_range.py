# -*- coding: utf-8 -*-
import maya.cmds as mc


def set_frame_range(start_frame, end_frame):
    mc.playbackOptions(min=start_frame, e=1)
    mc.playbackOptions(max=end_frame, e=1)
    mc.playbackOptions(ast=start_frame, e=1)
    mc.playbackOptions(aet=end_frame, e=1)
