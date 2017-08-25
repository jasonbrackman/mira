# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import delete_history
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        delete_history.delete_history(selected)
        self.pass_check(u"所有历史已被删除")

