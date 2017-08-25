# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"有显示层存在")
        else:
            self.pass_check(u"没有显示层存在")

    def get_error_list(self):
        display_layers = mc.ls(type="displayLayer")
        error_list = [layer for layer in display_layers if not layer == "defaultLayer"]
        return error_list

    def auto_solve(self):
        self.error_list = list()
        display_layers = self.get_error_list()
        for layer in display_layers:
            try:
                mc.delete(layer)
            except:
                self.error_list.append(layer)
        if self.error_list:
            self.fail_check(u"有些显示层不能被删除")
        else:
            self.pass_check(u"所有显示层已被删除")
