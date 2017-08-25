# -*- coding: utf-8 -*-
import pymel.core as pm
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        selected = pm.ls(sl=1)
        if not selected:
            self.fail_check(u"先选中模型大组")
            return
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"有模型选面赋材质")
        else:
            self.pass_check(u"没有模型选面赋材质")

    @staticmethod
    def get_error_list():
        sel = pm.ls(sl=1)[0]
        meshes = pm.listRelatives(sel, ad=1, type="mesh")
        invalid_meshes = list()
        for mesh in meshes:
            output_shading_engines = list(set(mesh.outputs(type="shadingEngine")))
            if len(output_shading_engines) > 1:
                invalid_meshes.append(mesh.name())
        return invalid_meshes


if __name__ == "__main__":
    pass
