# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_lay_structure(BaseCheck):

    def run(self):
        self.error_list = self.get_outer_group()
        if self.error_list:
            self.fail_check(u"文件打组不规范")
        else:
            self.pass_check(u"文件大纲规范")

    @staticmethod
    def get_outer_group():
        valid_group = ["persp", "top", "front", "side", "Camera", "Env", "_References"]
        outer_group = list()
        for group in mc.ls(assemblies=1):
            if group not in valid_group:
                outer_group.append(group)
        return outer_group
