# -*- coding: utf-8 -*-
import os
import maya.cmds as mc


def get_same_base_name_textures():
    wrong_files = list()
    files = mc.ls(type="file")
    if not files:
        return
    texture_names = [mc.getAttr("%s.computedFileTextureNamePattern" % f) for f in files]
    if not texture_names:
        return
    texture_names = list(set(texture_names))
    base_names = [os.path.basename(texture_name) for texture_name in texture_names]
    repeat_base_names = list()
    for base_name in base_names:
        num = base_names.count(base_name)
        if num > 1:
            repeat_base_names.append(base_name)
    if not repeat_base_names:
        return
    repeat_base_names = list(set(repeat_base_names))
    same_base_name_files = list()
    for base_name in repeat_base_names:
        temp_list = list()
        for texture_name in texture_names:
            if os.path.basename(texture_name) == base_name:
                temp_list.append(texture_name)
        same_base_name_files.append(temp_list)
    for i in same_base_name_files:
        if len(list(set(i))) != 1:
            wrong_files.extend(i)
    return wrong_files
