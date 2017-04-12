# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


attributes = ["castsShadows", "receiveShadows", "motionBlur", "primaryVisibility",
              "smoothShading", "visibleInReflections", "visibleInRefractions", "doubleSided"]


class check_mdl_render_property(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"有些模型的渲染属性未被打开")
        else:
            self.pass_check(u"所有模型的渲染属性都被打开")

    @staticmethod
    def get_error_list():
        selected = mc.ls(sl=1)[0]
        meshes = mc.listRelatives(selected, ad=1, type="mesh")
        invalid_meshes = list()
        if meshes:
            for mesh in meshes:
                status_list = list()
                for attribute in attributes:
                    status = mc.getAttr("%s.%s" % (mesh, attribute))
                    status_list.append(status)
                if not all(status_list):
                    invalid_meshes.append(mesh)
        return invalid_meshes

    def auto_solve(self):
        error_list = self.get_error_list()
        for mesh in error_list:
            for attr in attributes:
                mc.setAttr("%s.%s" % (mesh, attr), 1)
        self.pass_check(u"所有模型的渲染属性已被打开")


if __name__ == "__main__":
    pass
