# -*- coding: utf-8 -*-
import pymel.core as pm


def get_shader_history_nodes(node, include_self=True,
                             exclude_type=["mesh", "reference", "transform", "colorManagementGlobals"]):
    if not pm.objExists(node):
        print "%s is not an exist node"
        return
    if isinstance(node, basestring):
        node = pm.PyNode(node)
    history_node = list()

    def get_history_node(node):
        input_nodes = list(set(node.inputs()))
        if not input_nodes:
            return
        for input_node in input_nodes:
            if input_node.type() in exclude_type:
                continue
            history_node.append(input_node.name())
            get_history_node(input_node)
    get_history_node(node)
    if include_self:
        history_node.append(node.name())
    history_node = list(set(history_node))
    return history_node
