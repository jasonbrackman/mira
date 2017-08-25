# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs.pipeMaya import get_model_name
from BaseCheck import BaseCheck


class Check(BaseCheck):
    def __init__(self):
        super(Check, self).__init__()
        self.model_name = get_model_name.get_model_name()

    def run(self):
        selected_objects = mc.ls(sl=1)
        if selected_objects:
            if len(selected_objects) > 1:
                self.fail_check(u"不止一个物体被选中")
            elif len(selected_objects) == 1:
                if selected_objects[0] == self.model_name:
                    self.pass_check(u"%s被选中" % self.model_name)
                else:
                    self.fail_check(u"选中的物体不是模型大组:%s" % self.model_name)
        else:
            self.fail_check(u"%s模型大组没有被选中" % self.model_name)

    def auto_solve(self):
        if mc.objExists(self.model_name):
            mc.select(self.model_name, r=1)
            self.pass_check(u"模型大组没有被选中")
        else:
            self.fail_check(u"%s不存在" % self.model_name)
