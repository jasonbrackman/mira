# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.mayaLibs import unlock_normal


class Check(BaseCheck):

    def run(self):
        meshes = mc.ls(type="mesh")
        if not meshes:
            self.warning_check("No meshes found.")
        else:
            mc.select(meshes, r=1)
            unlock_normal.unlock_normal()
            self.pass_check(u"所有法线已被解锁。")
