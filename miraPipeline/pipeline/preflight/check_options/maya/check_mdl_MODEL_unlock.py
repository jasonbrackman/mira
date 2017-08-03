# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.pipeLibs.pipeMaya import get_model_name


class check_mdl_MODEL_unlock(BaseCheck):

    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"模型大组的位移旋转缩放信息被锁定")
        else:
            self.pass_check(u"模型大组的位移旋转缩放信息没有被锁定")

    def get_error_list(self):
        locked_attrs = list()
        base_attributes = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
        model_name = get_model_name.get_model_name()
        for attr in base_attributes:
            locked = mc.getAttr("%s.%s" % (model_name, attr), l=1)
            if locked:
                locked_attrs.append("%s.%s" % (model_name, attr))
        return locked_attrs

    def auto_solve(self):
        for attr in self.error_list:
            mc.setAttr(attr, l=0)
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"模型大组的位移旋转缩放信息被锁定")
        else:
            self.pass_check(u"模型大组的位移缩放旋转信息被解锁")