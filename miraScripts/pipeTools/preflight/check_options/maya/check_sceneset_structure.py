# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_sceneset_structure(BaseCheck):

    def run(self):
        if not mc.objExists("env"):
            self.fail_check("sceneset group is not exist.")
            return
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"大纲里有多余的组，应该只有env和prop")
        else:
            self.pass_check(u"大纲结构正确")

    @staticmethod
    def get_error_list():
        exclude = ['persp', 'top', 'front', 'side', "env", "prop"]
        top_groups = mc.ls(assemblies=1)
        wrong_list = list()
        for group in top_groups:
            if group not in exclude:
                wrong_list.append(group)
        return wrong_list
