# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_mdl_keyframe(BaseCheck):

    def run(self):
        self.error_list = self.get_anim_curves()
        if self.error_list:
            self.fail_check(u"有些模型有K帧")
        else:
            self.pass_check(u"所有模型均无K帧")

    def get_anim_curves(self):
        anim_curves = mc.ls(type="animCurve")
        return anim_curves

    def auto_solve(self):
        self.error_list = list()
        anim_curves = self.get_anim_curves()
        if not anim_curves:
            self.pass_check(u"所有模型均无K帧")
            return
        else:
            for curve in anim_curves:
                try:
                    mc.delete(curve)
                except:
                    self.error_list.append(curve)
        if self.error_list:
            self.fail_check(u"有些动画曲线不能被删除")
        else:
            self.pass_check(u"所有动画曲线已被删除")
