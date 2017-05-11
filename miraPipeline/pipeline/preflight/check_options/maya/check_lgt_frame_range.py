# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import set_frame_range
from miraLibs.pipeLibs.pipeMaya import get_valid_camera
from BaseCheck import BaseCheck


class check_lgt_frame_range(BaseCheck):

    def run(self):
        frame_range = self.get_frame_range()
        start_frame = int(mc.playbackOptions(q=1, min=1))
        end_frame = int(mc.playbackOptions(q=1, max=1))
        if frame_range == "%s-%s" % (start_frame, end_frame):
            self.pass_check(u"帧范围正确")
        else:
            self.fail_check(u"帧范围不正确")

    @staticmethod
    def get_frame_range():
        camera = get_valid_camera.get_valid_camera()
        frame_range = mc.getAttr("%s.frame_range" % camera)
        return frame_range

    def auto_solve(self):
        frame_range = self.get_frame_range()
        start, end = [int(value) for value in frame_range.split("-")]
        set_frame_range.set_frame_range(start, end)
