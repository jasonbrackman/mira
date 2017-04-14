# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_root_exist(BaseCheck):

    def run(self):
        if self.root_exist():
            self.pass_check(u"ROOT节点存在")
        else:
            self.fail_check(u"ROOT节点不存在，联系TD.")

    @staticmethod
    def root_exist():
        return mc.objExists("ROOT")
