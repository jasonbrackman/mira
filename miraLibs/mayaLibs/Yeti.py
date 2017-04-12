# -*- coding: utf-8 -*-
import os

import maya.cmds as mc


class Yeti(object):
    def __init__(self, node=None):
        self.node = node

    @staticmethod
    def get_all_yeti_nodes():
        return mc.ls(type="pgYetiMaya")

    @staticmethod
    def get_texture_path(yeti_node, texture_node):
        return mc.pgYetiGraph(yeti_node, node=texture_node, param="file_name", getParamValue=True)

    @staticmethod
    def set_texture_path(yeti_node, texture_node, new_texture_path):
        mc.pgYetiGraph(yeti_node, node=texture_node, param="file_name", setParamValueString=new_texture_path)

    @staticmethod
    def get_texture_nodes(yeti_node):
        texture_nodes = mc.pgYetiGraph(yeti_node, listNodes=True, type='texture')
        return texture_nodes

    def get_all_texture_path(self):
        textures = list()
        yeti_nodes = [self.node] if self.node is not None else self.get_all_yeti_nodes()
        if yeti_nodes:
            for yeti_node in yeti_nodes:
                texture_nodes = self.get_texture_nodes(yeti_node)
                if not texture_nodes:
                    continue
                for texture_node in texture_nodes:
                    texture_path = self.get_texture_path(yeti_node, texture_node)
                    textures.append(texture_path)
        return textures

    def set_all_texture_path(self, tex_dir):
        yeti_nodes = [self.node] if self.node is not None else self.get_all_yeti_nodes()
        if not yeti_nodes:
            return
        for yeti_node in yeti_nodes:
            texture_nodes = self.get_texture_nodes(yeti_node)
            if not texture_nodes:
                continue
            for texture_node in texture_nodes:
                tex_path = self.get_texture_path(yeti_node, texture_node)
                base_name = os.path.basename(tex_path)
                new_path = os.path.join(tex_dir, base_name).replace("\\", "/")
                self.set_texture_path(yeti_node, texture_node, new_path)
