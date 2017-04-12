# -*- coding: utf-8 -*-
import logging
import os
import maya.cmds as mc
from miraLibs.pyLibs import yml_operation
from miraLibs.mayaLibs import create_reference
from miraLibs.pipeLibs import pipeFile


logger = logging.getLogger(__name__)


class Node(object):
    def __init__(self, node):
        self.name = node
        self.node_type = None
        self.attr = dict()
        self.parent = None
        self.namespace = None

    def __str__(self):
        return self.name


def get_yml_data(yml_path):
    yml_data = yml_operation.get_yaml_data(yml_path)
    return yml_data


def build_group(node, parent):
    if not mc.objExists(node):
        mc.group(name=node, empty=1)
    if not parent:
        return
    else:
        if not mc.objExists(parent):
            mc.group(name=parent, empty=1)
    try:
        mc.parent(node, parent)
    except:pass


def set_attr(node, new_node=None):
    for attr in node.attr:
        if new_node:
            mc.setAttr("%s.%s" % (new_node, attr), node.attr[attr])
        else:
            mc.setAttr("%s.%s" % (node.name, attr), node.attr[attr])


def create_transform_node(transform_node):
    build_group(transform_node.name, transform_node.parent)
    set_attr(transform_node)


def get_model_group(reference_node):
    mdl_path = reference_node.mdl_path
    obj = pipeFile.PathDetails.parse_path(mdl_path)
    asset_type = obj.asset_type
    asset_name = obj.asset_name
    if asset_type == "environment":
        model_group = "env_%s_MODEL" % asset_name
    elif asset_type == "prop":
        model_group = "prop_%s_ROOT" % asset_name
    else:
        model_group = "char_%s_ROOT" % asset_name
    return model_group


def create_reference_node(reference_node):
    model_group = get_model_group(reference_node)
    outliner_name = "%s:%s" % (reference_node.namespace, model_group)
    if mc.objExists(outliner_name):
        set_attr(reference_node)
        build_group(outliner_name, reference_node.parent)
    else:
        if not os.path.isfile(reference_node.mdl_path):
            logger.error("%s is not an exist path" % reference_node.mdl_path)
            return
        try:
            new_node = create_reference.create_reference(reference_node.mdl_path, reference_node.namespace, True, True)
            set_attr(reference_node, new_node)
            build_group(new_node, reference_node.parent)
            logger.info("Create reference: %s successful." % reference_node.mdl_path)
        except:
            logger.error("Create reference: %s failed." % reference_node.mdl_path)


def rebuild_scene_with_path(yml_path):
    yml_data = get_yml_data(yml_path)
    for node in yml_data:
        node_obj = Node(node)
        node_dict = yml_data[node]
        node_obj.name = node
        node_obj.attr = node_dict["attr"]
        node_obj.parent = node_dict["parent"]
        node_obj.type = node_dict["type"]
        node_obj.namespace = node_dict["namespace"]
        node_obj.mdl_path = node_dict["mdl_path"]
        if node_obj.type == "transform":
            create_transform_node(node_obj)
        elif node_obj.type == "reference_model":
            create_reference_node(node_obj)


def rebuild_scene(path=None):
    obj = pipeFile.PathDetails.parse_path(path)
    seq = obj.seq
    project = obj.project
    connection_path = pipeFile.get_shot_step_connection_file(seq, "c000", "sceneset", project)
    if not os.path.isfile(connection_path):
        logger.error("%s is not an exist file." % connection_path)
        return False
    else:
        rebuild_scene_with_path(connection_path)
        return True


if __name__ == "__main__":
    rebuild_scene()
