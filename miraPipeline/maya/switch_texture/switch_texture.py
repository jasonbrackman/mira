# -*- coding: utf-8 -*-
import os
import pymel.core as pm


def get_dst_path(src, mode="half"):
    dst_path = None
    dir_name, basename = os.path.split(src)
    if mode == "half":
        if dir_name.endswith("half"):
            return
        dst_path = "%s/half/%s" % (dir_name, basename)
    else:
        if dir_name.endswith("half"):
            dst_path = "%s/%s" % (os.path.dirname(dir_name), basename)
    return dst_path


def switch_file_node_texture(mode):
    file_nodes = pm.ls(type="file")
    if not file_nodes:
        return
    for file_node in file_nodes:
        file_texture_name = file_node.fileTextureName.get()
        new_file_texture_name = get_dst_path(file_texture_name, mode)
        if new_file_texture_name:
            file_node.fileTextureName.set(new_file_texture_name)


def switch_rs_normal_texture(mode):
    normal_nodes = pm.ls(type="RedshiftNormalMap")
    if not normal_nodes:
        return
    for node in normal_nodes:
        texture_name = node.tex0.get()
        new_texture_name = get_dst_path(texture_name, mode)
        if new_texture_name:
            node.tex0.set(new_texture_name)


def switch_texture(mode):
    switch_file_node_texture(mode)
    switch_rs_normal_texture(mode)
