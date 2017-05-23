# -*- coding: utf-8 -*-
import nuke
from miraLibs.nukeLibs.get_all_input_nodes import get_all_input_nodes
from miraLibs.nukeLibs.get_format_of_read_node import get_format_of_read_node


def get_read_node_of_inputs(node):
    all_input_nodes = get_all_input_nodes(node)
    read_nodes = [input_node for input_node in all_input_nodes
                  if input_node.Class() == "Read" and not input_node["disable"].value()]
    return read_nodes


def get_frame_of_read_node(read_node):
    return int(read_node["last"].getValue())


def get_frame_hud(node):
    hud_frame_list = list()
    read_nodes = get_read_node_of_inputs(node)
    if not read_nodes:
        return
    for read_node in read_nodes:
        frame_list = get_frame_of_read_node(read_node)
        hud_frame_list.append(frame_list)
    frame_str = "%s/%s" % (nuke.frame(), max(hud_frame_list))
    return frame_str


def get_format_hud(node):
    hud_format_list = list()
    read_nodes = get_read_node_of_inputs(node)
    if not read_nodes:
        return
    for read_node in read_nodes:
        format_list = get_format_of_read_node(read_node)
        hud_format_list.append(format_list)
    format_str = max(set(hud_format_list), key=hud_format_list.count)
    return format_str


def get_hud(node):
    frame_str = get_frame_hud(node)
    format_str = get_format_hud(node)
    hud_str = "{:<12}{:<8}" .format(frame_str, format_str)
    return hud_str
