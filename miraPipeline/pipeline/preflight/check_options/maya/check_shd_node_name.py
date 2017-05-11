# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import get_shader_history_nodes, get_selected_group_sg
from miraLibs.pipeLibs import pipeFile
from BaseCheck import BaseCheck


class check_shd_node_name(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        prefix = self.get_prefix()
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"这些材质节点命名错误,必须以%s开始" % prefix)
        else:
            self.pass_check(u"所有材质节点命名正确")

    @staticmethod
    def get_created_sg_node():
        exclude_sg = ["initialParticleSE", "initialShadingGroup"]
        sg_nodes = get_selected_group_sg.get_selected_group_sg()
        created_sg = list(set(sg_nodes)-set(exclude_sg))
        return created_sg

    def get_error_list(self):
        error_list = list()
        prefix = self.get_prefix()
        create_sg = self.get_created_sg_node()
        if create_sg:
            for sg in create_sg:
                material_nodes = get_shader_history_nodes.get_shader_history_nodes(sg)
                if not material_nodes:
                    continue
                for material_node in material_nodes:
                    if not material_node.startswith(prefix):
                        error_list.append(material_node)
        return error_list

    @staticmethod
    def get_prefix():
        obj = pipeFile.PathDetails.parse_path()
        asset_name = obj.asset_name
        shd_version = obj.shd_version
        prefix = asset_name+"_"+shd_version+"_"
        return prefix

    def auto_solve(self):
        error_list = self.get_error_list()
        self.error_list = list()
        if error_list:
            prefix = self.get_prefix()
            for node in error_list:
                try:
                    new_name = "%s%s" % (prefix, node)
                    mc.rename(node, new_name)
                except:
                    self.error_list.append(node)
        if self.error_list:
            self.fail_check(u"有材质节点不能被命名正确")
        else:
            self.pass_check(u"所有材质节点被命名正确")
