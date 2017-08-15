# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.mayaLibs import delete_history


class check_mdl_intermediate(BaseCheck):

    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"有中间物体存在")
        else:
            self.pass_check(u"没有之间物体存在")

    @staticmethod
    def get_error_list():
        intermediate_objects = mc.ls(type="mesh", io=1)
        return intermediate_objects

    def auto_solve(self):
        intermediate_objects = self.get_error_list()
        delete_history.delete_history()
        try:
            mc.delete(intermediate_objects)
        except:pass
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"中间物体不能被删除,尝试导入reference.")
        else:
            self.pass_check(u"所有中间物体被删除")
