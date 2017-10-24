# -*- coding: utf-8 -*-
import os
import logging
import tempfile
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_scene_name, Yeti, get_all_hair_file_node, save_file, open_file
from miraLibs.pyLibs import join_path
from miraLibs.pipeLibs.copy import Copy


def get_temp_file(scene_name):
    base_name = os.path.basename(scene_name)
    temp_dir = tempfile.gettempdir()
    temp_file = join_path.join_path2(temp_dir, base_name)
    return temp_file


def get_yeti_textures():
    yt = Yeti.Yeti()
    yeti_textures = yt.get_all_texture_path()
    return yeti_textures


def set_yeti_textures(tex_dir):
    yt = Yeti.Yeti()
    yt.set_all_texture_path(tex_dir)


def get_hair_textures():
    textures = list()
    hair_file_nodes = get_all_hair_file_node.get_all_hair_file_node()
    if hair_file_nodes:
        textures = [mc.getAttr("%s.fileTextureName" % file_node) for file_node in hair_file_nodes]
    return textures


def set_hair_textures(tex_dir):
    hair_file_nodes = get_all_hair_file_node.get_all_hair_file_node()
    if not hair_file_nodes:
        return
    for file_node in hair_file_nodes:
        texture = mc.getAttr("%s.fileTextureName" % file_node)
        base_name = os.path.basename(texture)
        new_path = join_path.join_path2(tex_dir, base_name)
        mc.setAttr("%s.fileTextureName" % file_node, new_path, type="string")


def get_all_textures():
    yeti_textures = get_yeti_textures()
    hair_textures = get_hair_textures()
    return yeti_textures + hair_textures


def publish_textures(tex_dir):
    all_textures = get_all_textures()
    all_textures = list(set(all_textures))
    if not all_textures:
        return
    for tex in all_textures:
        base_name = os.path.basename(tex)
        new_path = join_path.join_path2(tex_dir, base_name)
        Copy.copy(tex, new_path)


def main():
    logger = logging.getLogger(__name__)
    obj = pipeFile.PathDetails.parse_path()
    tex_dir = obj.tex_dir
    work_path = obj.work_path
    # save to temp file
    scene_name = get_scene_name.get_scene_name()
    temp_file = get_temp_file(scene_name)
    Copy.copy(scene_name, temp_file)
    logger.info("save to temp file done.")
    # copy all textures to _tex
    publish_textures(tex_dir)
    set_hair_textures(tex_dir)
    set_yeti_textures(tex_dir)
    logger.info("publish texture done.")
    # save current file
    save_file.save_file()
    # copy to QCPublish path
    Copy.copy(scene_name, work_path)
    logger.info("copy to work path done.")
    # copy from temp file
    Copy.copy(temp_file, scene_name)
    # delete temp file
    os.remove(temp_file)
    # open scene name
    open_file.open_file(scene_name)
    logger.info("Reopen %s" % scene_name)
