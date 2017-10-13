# -*- coding: utf-8 -*-
import os
import pymel.core as pm
from miraLibs.mayaLibs import get_texture_real_path
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        file_nodes = pm.ls(type="file")
        # if has no file nodes ...return
        if not file_nodes:
            self.pass_check("No file node.")
            return
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"file节点的文件路径有误")
        else:
            self.pass_check(u"file节点文件路径正确")

    @staticmethod
    def get_error_list():
        invalid_files = list()
        file_nodes = pm.ls(type="file")
        for file_node in file_nodes:
            tex_path = file_node.computedFileTextureNamePattern.get()
            if not os.path.splitdrive(tex_path)[0]:
                tex_path = "%s/%s" % (pm.workspace.getPath(), tex_path)
            real_paths = get_texture_real_path.get_texture_real_path(tex_path)
            if not real_paths:
                invalid_files.append(file_node.name())
        normal_map_nodes = pm.ls(type="RedshiftNormalMap")
        if normal_map_nodes:
            for normal_map_node in normal_map_nodes:
                tex_path = normal_map_node.tex0.get()
                if not os.path.splitdrive(tex_path)[0]:
                    tex_path = "%s/%s" % (pm.workspace.getPath(), tex_path)
                real_paths = get_texture_real_path.get_texture_real_path(tex_path)
                if not real_paths:
                    invalid_files.append(normal_map_node.name())
        return invalid_files

if __name__ == "__main__":
    pass
