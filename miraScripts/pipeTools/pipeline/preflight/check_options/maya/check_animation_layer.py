# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_animation_layer(BaseCheck):

    def run(self):
        self.error_list = self.get_animation_layer()
        if self.error_list:
            self.fail_check(u"有动画层存在")
        else:
            self.pass_check(u"没有动画层存在")

    @staticmethod
    def get_animation_layer():
        return mc.ls(type="animLayer")

    def auto_solve(self):
        self.error_list = list()
        anim_layer = self.get_animation_layer()
        if anim_layer:
            for layer in anim_layer:
                try:
                    mc.delete(layer)
                except:
                    self.error_list.append(layer)
            if self.error_list:
                self.fail_check(u"有些动画层不能被删除")
            else:
                self.pass_check(u"所有动画层已被删除")
        else:
            self.pass_check(u"没有动画层存在")



if __name__ == "__main__":
    pass
