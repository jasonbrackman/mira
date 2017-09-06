# -*- coding: utf-8 -*-
import pymel.core as pm
from BaseCheck import BaseCheck
import maya.mel as mel
import miraCore


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

    def auto_solve(self):
        mira_dir = miraCore.mira_dir
        mel_path = "%s/miraLibs/mayaLibs/rename_duplicate.mel" % mira_dir
        mel_path = mel_path.replace("\\", "/")
        mel.eval("source \"%s\"" % mel_path)
        self.error_list = self.get_all_duplicate_names()
        if self.error_list:
            self.fail_check("Some nodes can't be corrected.")
        else:
            self.pass_check("All duplicate node corrected.")
