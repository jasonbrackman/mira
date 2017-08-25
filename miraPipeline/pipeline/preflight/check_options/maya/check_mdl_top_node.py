# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        top_nodes = mc.ls(assemblies=1)
        selected = mc.ls(sl=1)
        if len(selected) != 1:
            self.fail_check(u"不止一个模型被选中")
            return
        if selected[0] in top_nodes:
            self.pass_check(u"模型大组在最顶层")
        else:
            self.fail_check(u"模型大组不在最顶层")
