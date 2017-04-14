# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mel
from BaseCheck import BaseCheck


class check_mdl_unsew_vertex(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        self.error_list = self.get_unsew_vertex()
        if self.error_list:
            self.fail_check(u"有没缝合的点")
        else:
            self.pass_check(u"没有没缝合的点")

    @staticmethod
    def get_unsew_vertex():
        edges = mel.eval('polyCleanupArgList 3 '
                         '{ "0","2","1","0","0","0","0","0","0",'
                         '"1e-005","1","0.1","0","1e-005","0","-1","0" };')
        if not edges:
            return
        vertex = mc.polyListComponentConversion(edges, tv=1)
        return vertex
