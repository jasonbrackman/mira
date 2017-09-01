# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import delete_render_layer
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        self.error_list = self.get_render_layer()
        if self.error_list:
            self.fail_check(u"有渲染层的存在")
        else:
            self.pass_check(u"没有渲染层的存在")

    @staticmethod
    def get_render_layer():
        all_layer = mc.ls(type="renderLayer")
        invalid_renderlayer = [layer for layer in all_layer if not layer == "defaultRenderLayer"]
        return invalid_renderlayer

    def auto_solve(self):
        render_layers = self.get_render_layer()
        for layer in render_layers:
            delete_render_layer.delete_render_layer(layer)
        self.pass_check(u"所有渲染层已被删除")
