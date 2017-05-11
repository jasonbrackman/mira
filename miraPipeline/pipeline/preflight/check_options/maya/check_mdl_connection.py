# -*- coding: utf-8 -*-
import pymel.core as pm
from BaseCheck import BaseCheck


class check_mdl_connection(BaseCheck):

    def run(self):
        selected = pm.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        self.error_list = self.get_connection_attributes()
        if self.error_list:
            self.fail_check(u"模型位移缩放旋转属性上有连接")
        else:
            self.pass_check(u"模型位移缩放旋转属性没有连接")

    @staticmethod
    def get_connection_attributes():
        base_attributes = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
        has_connection_attributes = list()
        selected = pm.ls(sl=1)[0]
        meshes = selected.getChildren(allDescendents=True, type="mesh")
        transforms = [mesh.getParent() for mesh in meshes]
        for transform in transforms:
            for attr in base_attributes:
                attr_name = "%s.%s" % (transform.name(), attr)
                connections = pm.PyNode(attr_name).connections()
                if connections:
                    has_connection_attributes.append(attr_name)
        return has_connection_attributes
