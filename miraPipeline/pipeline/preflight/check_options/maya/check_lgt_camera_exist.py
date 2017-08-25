# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs.pipeMaya import get_valid_camera
from BaseCheck import BaseCheck


class Check(BaseCheck):
    def run(self):
        valid_camera = get_valid_camera.get_valid_camera()
        if not valid_camera:
            self.fail_check(u"摄像机不存在")
        else:
            if mc.ls("%s.frame_range" % valid_camera):
                self.pass_check(u"摄像机正确")
            else:
                self.fail_check(u"摄像机没有frame_range属性")
