# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import join_path
from miraLibs.mayaLibs import get_texture_real_path
from miraLibs.pyLibs import copy


logger = logging.getLogger(__name__)


def export_shd_textures(change_file_texture_name=True):
    context = pipeFile.PathDetails.parse_path()
    tex_dir = context.tex_dir
    export_file_node_textures(tex_dir, change_file_texture_name)
    export_rs_normal_map_textures(tex_dir, change_file_texture_name)


def export_rs_normal_map_textures(tex_dir, change_file_texture_name):
    rs_normal_maps = mc.ls(type="RedshiftNormalMap")
    if not rs_normal_maps:
        return
    for normal_map in rs_normal_maps:
        texture = mc.getAttr("%s.tex0" % normal_map)
        if not texture:
            continue
        texture = texture.replace("\\", "/")
        if not os.path.splitdrive(texture)[0]:
            texture = "%s%s" % (mc.workspace(q=1, rootDirectory=1, fullName=1), texture)
        real_path = get_texture_real_path.get_texture_real_path(texture)
        if not real_path:
            continue
        for each_path in real_path:
            base_name = os.path.basename(each_path)
            new_path = join_path.join_path2(tex_dir, base_name)
            if copy.copy(each_path, new_path):
                logger.info("Copy %s >> %s" % (each_path, new_path))
        if change_file_texture_name:
            texture_base_name = os.path.basename(texture)
            new_texture_path = join_path.join_path2(tex_dir, texture_base_name)
            mc.setAttr("%s.tex0" % normal_map, new_texture_path, type="string")


def export_file_node_textures(tex_dir, change_file_texture_name):
    file_nodes = mc.ls(type="file")
    if not file_nodes:
        return
    for file_node in file_nodes:
        texture = mc.getAttr("%s.computedFileTextureNamePattern" % file_node)
        if not texture:
            continue
        texture = texture.replace("\\", "/")
        if not os.path.splitdrive(texture)[0]:
            texture = "%s%s" % (mc.workspace(q=1, rootDirectory=1, fullName=1), texture)
        real_path = get_texture_real_path.get_texture_real_path(texture)
        if not real_path:
            continue
        for each_path in real_path:
            base_name = os.path.basename(each_path)
            new_path = join_path.join_path2(tex_dir, base_name)
            if copy.copy(each_path, new_path):
                logger.info("Copy %s >> %s" % (each_path, new_path))
        if change_file_texture_name:
            texture_base_name = os.path.basename(texture)
            new_texture_path = join_path.join_path2(tex_dir, texture_base_name)
            mc.setAttr("%s.fileTextureName" % file_node, new_texture_path, type="string")


if __name__ == "__main__":
    export_shd_textures()
