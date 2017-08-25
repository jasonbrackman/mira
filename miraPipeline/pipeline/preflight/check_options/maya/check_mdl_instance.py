# -*- coding: utf-8 -*-
import pymel.core as pm
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        selected = pm.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        self.error_list = self.get_instance_meshes()
        if self.error_list:
            self.fail_check(u"有关联复制的模型存在")
        else:
            self.pass_check(u"没有关联复制的模型存在")

    @staticmethod
    def get_instance_meshes():
        selected = pm.ls(sl=1)[0]
        meshes = selected.getChildren(allDescendents=True, type="mesh")
        instance_meshes = list()
        for mesh in meshes:
            mesh_parent = pm.listRelatives(mesh, ap=1)
            if len(mesh_parent) > 1:
                instance_meshes.append(mesh.name())
        return instance_meshes
