# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        model_group = self.get_model_group()
        if len(model_group) > 1:
            self.error_list = model_group
        if self.error_list:
            self.fail_check(u"模型大组下有以_MODEL结尾的")
        else:
            self.pass_check(u"模型大组下没有以_MODEL结尾的")

    @staticmethod
    def get_model_group():
        selected = mc.ls(sl=1)
        children = mc.listRelatives(selected[0], ad=1, type="transform")
        children.append(selected[0])
        error_list = [child for child in children if child.endswith("_MODEL")]
        return error_list
