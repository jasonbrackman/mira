# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_frame_range


class Check(BaseCheck):
    def __init__(self):
        super(Check, self).__init__()
        self.valid_camera = self.get_valid_camera()
        start_frame, end_frame = get_frame_range.get_frame_range()
        self.frame_range = "%s-%s" % (start_frame, end_frame)

    def run(self):
        attr_frame_range = mc.getAttr("%s.frame_range" % self.valid_camera)
        if attr_frame_range == self.frame_range:
            self.pass_check(u"摄像机的frame_range属性值设置正确")
        else:
            self.fail_check(u"摄像机的frame_range属性值与当前镜头的帧区间不一致")

    @staticmethod
    def get_valid_camera():
        obj = pipeFile.PathDetails.parse_path()
        seq = obj.seq
        shot = obj.shot
        valid_camera = "cam_%s_%s" % (seq, shot)
        return valid_camera

    def auto_solve(self):
        mc.lockNode(self.valid_camera, lock=0)
        mc.setAttr("%s.frame_range" % self.valid_camera, lock=0)
        mc.setAttr("%s.frame_range" % self.valid_camera, self.frame_range, type="string")
        mc.setAttr("%s.frame_range" % self.valid_camera, lock=1)
        self.pass_check(u"帧范围设置正确")
