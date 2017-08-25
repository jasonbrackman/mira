# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        meshes = mc.ls(type="mesh", long=1)
        if not meshes:
            self.warning_check("No meshes.")
            return
        for mesh in meshes:
            mc.displaySmoothness(mesh, polygonObject=1)
        self.pass_check(u"所有模型处于按1的状态")
