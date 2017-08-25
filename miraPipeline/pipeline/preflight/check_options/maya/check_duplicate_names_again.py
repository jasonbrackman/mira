# -*- coding: utf-8 -*-
import pymel.core as pm
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        all_duplicate_names = self.get_all_duplicate_names()
        if all_duplicate_names:
            self.error_list = all_duplicate_names
            self.fail_check(u"有同名物体存在")
        else:
            self.pass_check(u"没有同名物体存在")

    @staticmethod
    def get_all_duplicate_names():
        all_duplicate_names = []
        all_maya_obj = pm.ls()
        for maya_obj in all_maya_obj:
            if maya_obj.find('|') > -1:
                all_duplicate_names.append(str(maya_obj.name()))
        return all_duplicate_names
