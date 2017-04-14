# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_start_frame(BaseCheck):

    def run(self):
        start_frame = mc.playbackOptions(q=1, minTime=1)
        if int(start_frame) == 101:
            self.pass_check(u"镜头从101帧开始。")
        else:
            self.fail_check(u"镜头不是从101帧开始")
