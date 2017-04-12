# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_all_parent_nodes(node, include_self=False):
    parent_nodes = list()

    def get_parent_node(node):
        parent_node = mc.listRelatives(node, p=1)
        if not parent_node:
            return
        parent_nodes.extend(parent_node)
        for node in parent_node:
            get_parent_node(node)
    get_parent_node(node)
    if include_self:
        parent_nodes.append(node)
    return list(set(parent_nodes))
