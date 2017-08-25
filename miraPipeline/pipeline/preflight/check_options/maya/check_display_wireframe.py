# -*- coding: utf-8 -*-
from miraLibs.mayaLibs import display_wireframe
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        try:
            display_wireframe.display_wireframe()
            self.pass_check(u"display wireframe<线框显示>")
        except:
            self.fail_check("Something wrong with display wireframe")
