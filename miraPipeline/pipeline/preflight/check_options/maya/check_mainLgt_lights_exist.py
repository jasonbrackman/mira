# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        outer = mc.ls(assemblies=1)
        if "Lights" in outer:
            self.pass_check("Lights group exist")
        else:
            self.fail_check("Lights group not exist.")
