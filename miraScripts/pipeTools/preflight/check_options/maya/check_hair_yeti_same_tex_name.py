# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from miraLibs.mayaLibs import Yeti
from BaseCheck import BaseCheck


class check_hair_yeti_same_tex_name(BaseCheck):
    def __init__(self):
        super(check_hair_yeti_same_tex_name, self).__init__()
        self.yeti_nodes = mc.ls(type="pgYetiMaya")

    def run(self):
        if not self.yeti_nodes:
            self.pass_check(u"没有pgyetiMaya节点存在")
            return
        self.error_list = self.get_same_tex()
        if self.error_list:
            self.fail_check(u"这些贴图有相同的名字")
        else:
            self.pass_check(u"所有的yeti毛发贴图没有相同的名字")

    def get_same_tex(self):
        error_list = list()
        yt = Yeti.Yeti()
        all_textures = yt.get_all_texture_path()
        if not all_textures:
            return
        error_base_names = self.get_error_base_names(all_textures)
        if not error_base_names:
            return
        for tex in all_textures:
            if os.path.basename(tex) in error_base_names:
                error_list.append(tex)
        return error_list

    @staticmethod
    def get_error_base_names(textures):
        error_base_names = list()
        base_names = [os.path.basename(tex) for tex in textures]
        for base_name in base_names:
            count = base_names.count(base_name)
            if count > 1:
                error_base_names.append(base_name)
        return error_base_names
