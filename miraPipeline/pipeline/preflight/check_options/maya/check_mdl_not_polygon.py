# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_mdl_not_polygon(BaseCheck):

    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"有模型不是polygon")
        else:
            self.pass_check(u"所有模型都是polygon")

    @staticmethod
    def get_error_list():
        geometries = mc.ls(geometry=1, l=1)
        invalid_meshes = [geometry for geometry in geometries if mc.nodeType(geometry) not in ["mesh"]]
        return invalid_meshes
