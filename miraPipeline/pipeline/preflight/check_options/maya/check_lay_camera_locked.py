# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs.pipeMaya import get_valid_camera
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        self.error_list = self.get_unclock_attrs()
        if self.error_list:
            self.fail_check(u"摄像机未锁定")
        else:
            self.pass_check(u"摄像机已被锁定")

    def get_unclock_attrs(self):
        unlock_attrs = list()
        base_attributes = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
        camera = get_valid_camera.get_valid_camera()
        for attr in base_attributes:
            attr_name = "%s.%s" % (camera, attr)
            if not mc.getAttr(attr_name, l=1):
                unlock_attrs.append(attr_name)
        return unlock_attrs

    def auto_solve(self):
        self.error_list = list()
        unlock_attrs = self.get_unclock_attrs()
        for attr in unlock_attrs:
            try:
                mc.setAttr(attr, l=1)
            except:
                self.error_list.append(attr)
        if self.error_list:
            self.fail_check(u"有些属性不能被锁定")
        else:
            self.pass_check(u"摄像机已被锁定")
