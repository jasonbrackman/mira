# -*- coding: utf-8 -*-
import pymel.core as pm


def get_file_textures():
    file_nodes = pm.ls(type="file")
    if not file_nodes:
        return
    file_textures = list()
    for file_node in file_nodes:
        file_texture_name = file_node.fileTextureName.get()
        file_texture_name = file_texture_name.replace("\\", "/")
        file_textures.append(file_texture_name)
    return file_textures


if __name__ == "__main__":
    pass
