# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_mdl_suffix(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        self.error_list = self.get_invalid_meshes()
        if self.error_list:
            self.fail_check(u"有模型shape命名不正确")
        else:
            self.pass_check(u"模型命名正确")

    @staticmethod
    def get_invalid_meshes():
        invalid_meshes = list()
        selected = mc.ls(sl=1)[0]
        meshes = mc.listRelatives(selected, ad=1, type="mesh")
        transforms = list(set(mc.listRelatives(meshes, parent=1)))
        for transform in transforms:
            shape = mc.listRelatives(transform, s=1)[0]
            if shape == "%s_GEOSHAPE" % transform:
                continue
            invalid_meshes.append(shape)
        return invalid_meshes

    def auto_solve(self):
        self.error_list = list()
        invalid_meshes = self.get_invalid_meshes()
        for mesh in invalid_meshes:
            transform = mc.listRelatives(mesh, parent=1)[0]
            mc.rename(mesh, "%s_GEOSHAPE" % transform)
        self.error_list = self.get_invalid_meshes()
        if self.error_list:
            self.fail_check(u"有些模型不能更改名字")
        else:
            self.pass_check(u"所有模型命名正确")
