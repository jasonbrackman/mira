# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import join_path
from miraLibs.mayaLibs import get_texture_real_path
from miraLibs.pipeLibs.copy import Copy


def export_shd_textures(change_file_texture_name=True):
    logger = logging.getLogger(__name__)
    file_nodes = mc.ls(type="file")
    if not file_nodes:
        return
    obj = pipeFile.PathDetails.parse_path()
    texture_dir = obj.tex_dir
    for file_node in file_nodes:
        texture = mc.getAttr("%s.computedFileTextureNamePattern" % file_node)
        if not texture:
            continue
        texture = texture.replace("\\", "/")
        real_path = get_texture_real_path.get_texture_real_path(texture)
        if not real_path:
            continue
        for each_path in real_path:
            base_name = os.path.basename(each_path)
            new_path = join_path.join_path2(texture_dir, base_name)
            if Copy.copy(each_path, new_path):
                logger.info("Copy %s >> %s" % (each_path, new_path))
        if change_file_texture_name:
            texture_base_name = os.path.basename(texture)
            new_texture_path = join_path.join_path2(texture_dir, texture_base_name)
            mc.setAttr("%s.fileTextureName" % file_node, new_texture_path, type="string")


if __name__ == "__main__":
    export_shd_textures()
