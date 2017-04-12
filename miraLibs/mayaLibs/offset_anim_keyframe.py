# -*- coding: utf-8 -*-
import maya.cmds as mc


def offset_anim_keyframe(anim_curves, frame_offset):
    mc.keyframe(anim_curves, e=1, includeUpperBound=True, option='over', relative=1, timeChange=frame_offset)


if __name__ == "__main__":
    pass
