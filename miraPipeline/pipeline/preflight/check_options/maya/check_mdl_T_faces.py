# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mel
from BaseCheck import BaseCheck


class check_mdl_T_faces(BaseCheck):

    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"有T形面存在")
        else:
            self.pass_check(u"没有T形面存在")

    @staticmethod
    def get_error_list():
        selected = mc.ls(sl=1)
        t_faces = mel.eval('polyCleanupArgList 3 '
                           '{ "0","2","1","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","1","0" };')
        mc.select(selected)
        return t_faces
