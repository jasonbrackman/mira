# -*- coding: utf-8 -*-
import maya.cmds as mc
import get_objs_in_camera_view


def get_reference_nodes_in_obj_list(obj_list):
    reference_nodes = []
    for obj in obj_list:
        if not mc.referenceQuery(obj, isNodeReferenced=1):
            continue
        reference_node = mc.referenceQuery(obj, referenceNode=True)
        if reference_node:
            reference_nodes.append(reference_node)
    reference_nodes = list(set(reference_nodes))
    return reference_nodes


def get_reference_nodes_in_camera_view(camera_name, min_frame, max_frame):
    obj_list = get_objs_in_camera_view.get_objs_in_camera_view(camera_name, min_frame, max_frame)
    reference_nodes = get_reference_nodes_in_obj_list(obj_list)
    return reference_nodes


if __name__ == "__main__":
    pass
