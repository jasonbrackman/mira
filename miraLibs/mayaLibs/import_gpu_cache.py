# -*- coding: utf-8 -*-
import maya.cmds as mc


def import_gpu_cache(gpu_name, parent_name, cache_file_name):
    """
    :param gpu_name: gpu shape node name
    :param parent_name: gpu node name
    :param cache_file_name: gpu cache file name
    :return:
    """
    gpu_node = mc.createNode("gpuCache", name=gpu_name)
    mc.setAttr("%s.cacheFileName" % gpu_node, cache_file_name, type="string")
    parent_node = mc.listRelatives(gpu_node, parent=1)[0]
    final_name = mc.rename(parent_node, parent_name)
    return final_name
