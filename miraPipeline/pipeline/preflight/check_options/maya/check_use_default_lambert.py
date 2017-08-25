# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):
    def run(self):
        self.error_list = self.get_obj_assign_default_lambert()
        if self.error_list:
            self.fail_check(u"有模型赋予lambert1材质球")
        else:
            self.pass_check(u"没有模型赋予lambert1材质球")

    @staticmethod
    def get_obj_assign_default_lambert():
        objects = mc.listConnections("initialShadingGroup", s=1, d=0, type="mesh")
        return objects
