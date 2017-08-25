# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"有多个uv set存在")
        else:
            self.pass_check(u"没有多个uv set存在")

    @staticmethod
    def get_error_list():
        uv_sets = mc.polyUVSet(q=1, allUVSets=1)
        if uv_sets and len(uv_sets) > 1:
            return uv_sets
