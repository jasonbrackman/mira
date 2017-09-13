# -*- coding: utf-8 -*-
import maya.cmds as mc
import xgenm as xgen
from BaseCheck import BaseCheck
from miraLibs.mayaLibs import get_shader_history_nodes
from miraLibs.pipeLibs import pipeFile


class Check(BaseCheck):

    def __init__(self):
        BaseCheck.__init__(self)
        self.prefix = self.get_prefix()

    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"这些材质节点命名不正确")
        else:
            self.pass_check(u"所有材质节点命名正确")

    @staticmethod
    def get_descriptions():
        collections = xgen.palettes()
        needed_collection = collections[0]
        descriptions = xgen.descriptions(needed_collection)
        return descriptions

    def get_all_hair_sg_nodes(self):
        hair_sg_nodes = list()
        descriptions = self.get_descriptions()
        if not descriptions:
            return
        for description in descriptions:
            shapes = mc.listRelatives(description, s=1)
            if not shapes:
                continue
            shape = shapes[0]
            sg_nodes = mc.listConnections(shape, s=0, d=1, type="shadingEngine")
            if not sg_nodes:
                continue
            sg_node = sg_nodes[0]
            hair_sg_nodes.append(sg_node)
            hair_sg_nodes = list(set(hair_sg_nodes))
        return hair_sg_nodes

    def get_all_hair_mat_nodes(self):
        mat_nodes = list()
        sg_nodes = self.get_all_hair_sg_nodes()
        if not sg_nodes:
            return
        for sg_node in sg_nodes:
            mat_node_list = get_shader_history_nodes.get_shader_history_nodes(sg_node, True)
            if mat_node_list:
                mat_nodes.extend(mat_node_list)
        return mat_nodes

    @staticmethod
    def get_prefix():
        context = pipeFile.PathDetails.parse_path()
        asset_name = context.asset_name
        task = context.task
        prefix = "%s_%s_" % (asset_name, task)
        return prefix

    def get_error_list(self):
        error_list = list()
        mat_nodes = self.get_all_hair_mat_nodes()
        if not mat_nodes:
            return
        prefix = self.prefix
        for mat_node in mat_nodes:
            if not mat_node.startswith(prefix):
                error_list.append(mat_node)
        return error_list

    def auto_solve(self):
        error_list = self.get_error_list()
        for node in error_list:
            try:
                mc.rename(node, "%s%s" % (self.prefix, node))
            except:
                print "%s can not be renamed" % node
        self.pass_check(u"所有毛发材质节点已被命名正确")
