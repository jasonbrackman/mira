# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_frame_range():
    first_frame = mc.playbackOptions(q=1, min=1)
    end_frame = mc.playbackOptions(q=1, max=1)
    return int(first_frame), int(end_frame)


if __name__ == "__main__":
    pass
