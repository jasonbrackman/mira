# -*- coding: utf-8 -*-
import pymel.core as pm


def get_file_node_textures():
    file_nodes = pm.ls(type="file")
    file_textures = list()
    if file_nodes:
        for file_node in file_nodes:
            file_texture_name = file_node.fileTextureName.get()
            if not file_texture_name:
                continue
            file_texture_name = file_texture_name.replace("\\", "/")
            file_textures.append(file_texture_name)
    return file_textures


def get_rs_normal_textures():
    rs_normal_nodes = pm.ls(type="RedshiftNormalMap")
    textures = list()
    if rs_normal_nodes:
        for node in rs_normal_nodes:
            texture_name = node.tex0.get()
            if not texture_name:
                continue
            texture_name = texture_name.replace("\\", "/")
            textures.append(texture_name)
    return textures


def get_file_textures():
    textures = get_file_node_textures() + get_rs_normal_textures()
    textures = list(set(textures))
    return textures


if __name__ == "__main__":
    pass
