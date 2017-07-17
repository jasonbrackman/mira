# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class check_group_structure(BaseCheck):

    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"大纲里有节点不是assemblyReference节点")
        else:
            self.pass_check("All is assemblyReference.")

    @staticmethod
    def get_error_list():
        all_assemblies_nodes = mc.ls(assemblies=1)
        camera_nodes = ['persp', 'top', 'front', 'side']
        created_nodes = list(set(all_assemblies_nodes)-set(camera_nodes))
        error_nodes = [node for node in created_nodes if mc.nodeType(node) != "assemblyReference"]
        return error_nodes

    def auto_solve(self):
        self.error_list = list()
        error_list = self.get_error_list()
        for node in error_list:
            try:
                mc.delete(node)
            except:
                self.error_list.append(node)
        if self.error_list:
            self.fail_check(u"这些节点不能被删除。")
        else:
            self.pass_check(u"assemblyReference之外的节点被删除。")
