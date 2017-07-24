# -*- coding: utf-8 -*-
import maya.mel as mel
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_mdl_cleanup(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        self.error_list = self.get_error_faces()
        if self.error_list:
            self.fail_check(u"有五边面、T形面、没缝合的点存在。")
        else:
            self.pass_check(u"模型合法")

    @staticmethod
    def get_error_faces():
        selected = mc.ls(sl=1)
        error_faces = mel.eval('polyCleanupArgList 4 '
                               '{ "0","2","1","0","1","0","1","0","0","1e-005","1","0.001","0",'
                               '"1e-005","0","-1","1","0" };')
        mc.select(selected)
        return error_faces
