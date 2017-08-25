# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import get_selected_group_sg, get_shader_history_nodes
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        self.error_list = self.get_referenced_material()
        if self.error_list:
            self.fail_check(u"有些材质球是reference进来的")
        else:
            self.pass_check(u"没有reference进来任何材质球")

    @staticmethod
    def get_referenced_material():
        referenced_material = list()
        sg_nodes = get_selected_group_sg.get_selected_group_sg()
        shd_nodes = list()
        for sg in sg_nodes:
            history_node = get_shader_history_nodes.get_shader_history_nodes(sg)
            if not history_node:
                continue
            shd_nodes.extend(history_node)
        shd_nodes = list(set(shd_nodes))
        if shd_nodes:
            referenced_material = [node for node in shd_nodes if mc.referenceQuery(node, isNodeReferenced=1)]
        return referenced_material
