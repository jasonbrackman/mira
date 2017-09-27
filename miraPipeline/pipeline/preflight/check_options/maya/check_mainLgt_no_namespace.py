# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"这些灯光有namespace存在")
        else:
            self.pass_check(u"所有灯光没有namespace存在")

    @staticmethod
    def get_error_list():
        lights = mc.listRelatives("Lights", ad=1)
        if not lights:
            return
        error_list = [light for light in lights if ":" in light]
        return error_list
