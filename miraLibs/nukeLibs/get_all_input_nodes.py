# -*- coding: utf-8 -*-
import nuke


def get_all_input_nodes(node):
    all_nodes = list()

    def get_input_nodes(node):
        input_nodes = node.dependencies(nuke.INPUTS)
        if input_nodes:
            all_nodes.extend(input_nodes)
            for input_node in input_nodes:
                get_input_nodes(input_node)

    get_input_nodes(node)
    return all_nodes
