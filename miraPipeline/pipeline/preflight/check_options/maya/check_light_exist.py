# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import get_all_lights
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        self.error_list = get_all_lights.get_all_lights()
        if self.error_list:
            self.fail_check(u"有灯光存在")
        else:
            self.pass_check(u"没有灯光存在")

    def auto_solve(self):
        self.error_list = list()
        lights = get_all_lights.get_all_lights()
        for light in lights:
            try:
                mc.lockNode(light, l=0)
                mc.delete(light)
            except:
                self.error_list.append(light)
        if self.error_list:
            self.fail_check(u"有些灯光删不掉，请手动删除")
        else:
            self.pass_check(u"所有灯光已被删除")
