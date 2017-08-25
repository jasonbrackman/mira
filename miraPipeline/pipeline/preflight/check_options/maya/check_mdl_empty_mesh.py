# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import delete_models
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        self.error_list = self.get_empty_mesh()
        if self.error_list:
            self.fail_check(u"有无面模型")
        else:
            self.pass_check(u"没有无面模型")

    @staticmethod
    def get_empty_mesh():
        selected = mc.ls(sl=1)
        meshes = mc.listRelatives(selected[0], ad=1, type="mesh", fullPath=1)
        empty_meshes = [mesh for mesh in meshes if not mc.polyEvaluate(mesh, f=1)]
        return empty_meshes

    def auto_solve(self):
        self.error_list = list()
        empty_meshes = self.get_empty_mesh()
        for mesh in empty_meshes:
            try:
                delete_models.delete_models(mesh)
            except:
                self.error_list.append(mesh)
        if self.error_list:
            self.fail_check(u"有些无面模型不能被删除")
        else:
            self.pass_check(u"所有无面模型已被删除")
