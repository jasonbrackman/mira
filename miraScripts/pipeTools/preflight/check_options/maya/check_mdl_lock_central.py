# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import lock_central_pivot
from miraLibs.pipeLibs.pipeMaya import get_model_name
from BaseCheck import BaseCheck


class check_mdl_lock_central(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        unlock_attrs = self.get_lock_attr()
        if unlock_attrs:
            self.error_list = unlock_attrs
            self.fail_check(u"模型中心坐标未锁定")
        else:
            self.pass_check(u"模型中心坐标处于锁定状态")

    def get_lock_attr(self):
        model_name = mc.ls(sl=1)[0]
        attrs = ["%s.rotatePivot" % model_name, "%s.scalePivot" % model_name]
        unlock_attrs = [attr for attr in attrs if not mc.getAttr(attr, l=1)]
        return unlock_attrs

    def auto_solve(self):
        model_name = mc.ls(sl=1)[0]
        lock_central_pivot.lock_central_pivot(model_name)
        self.pass_check(u"模型中心坐标已被锁定")