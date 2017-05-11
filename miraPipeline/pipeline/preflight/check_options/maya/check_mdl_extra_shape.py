# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_mdl_extra_shape(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        self.error_list = self.get_invalid_transform()
        if self.error_list:
            self.fail_check(u"一个transform下有多个shape")
        else:
            self.pass_check(u"transform下没有多余的shape")

    @staticmethod
    def get_invalid_transform():
        selected = mc.ls(sl=1)[0]
        meshes = mc.listRelatives(selected, ad=1, type="mesh")
        transforms = mc.listRelatives(meshes, parent=1)
        transforms = list(set(transforms))
        invalid_transform = list()
        for transform in transforms:
            children = mc.listRelatives(transform, children=1)
            if len(children) > 1:
                invalid_transform.append(transform)
        invalid_transform = list(set(invalid_transform))
        return invalid_transform
