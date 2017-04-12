# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pyLibs import yml_operation
from miraLibs.mayaLibs import get_all_parent_nodes, get_namespace
from miraLibs.pipeLibs.pipeMaya import get_models


BASE_ATTRIBUTES = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']


class Node(object):
    def __init__(self, node):
        self.name = node
        self.node_type = None
        self.attr = dict()
        self.parent = None
        self.namespace = None
        self.mdl_path = None

    def get_node_info(self):
        self.attr = self.get_attr_dict()
        if self.name.endswith("_MODEL") or self.name.endswith("_ROOT"):
            self.node_type = "reference_model"
            self.namespace = str(get_namespace.get_namespace(self.name))
            self.mdl_path = self.get_mdl_path()
        else:
            self.node_type = "transform"
        self.parent = self.get_parent()

    def get_attr_dict(self):
        attr_dict = dict()
        if mc.nodeType(self.name) == "transform":
            for attr in BASE_ATTRIBUTES:
                value = mc.getAttr("%s.%s" % (self.name, attr))
                attr_dict[attr] = value
        return attr_dict

    def get_parent(self):
        parent_node = mc.listRelatives(self.name, p=1)
        if parent_node:
            return str(parent_node[0])

    def get_mdl_path(self):
        mdl_path = mc.referenceQuery(self.name, filename=1, withoutCopyNumber=1)
        return str(mdl_path)

    def parse_node(self):
        self.get_node_info()
        node_dict = dict()
        node_dict["type"] = self.node_type
        node_dict["attr"] = self.attr
        node_dict["parent"] = self.parent
        node_dict["mdl_path"] = self.mdl_path
        node_dict["namespace"] = self.namespace
        return node_dict


def get_root_node(model):
    root_node = None
    parent_nodes = get_all_parent_nodes.get_all_parent_nodes(model)
    for parent_node in parent_nodes:
        if parent_node.endswith("_ROOT"):
            root_node = parent_node
            break
    return root_node


def get_all_out_nodes():
    all_out_nodes = list()
    models = get_models.get_models()
    if not models:
        return
    for model in models:
        root_node = get_root_node(model)
        node = root_node if root_node else model
        parent_node = get_all_parent_nodes.get_all_parent_nodes(node, True)
        all_out_nodes.extend(parent_node)
    return list(set(all_out_nodes))


def export_scene(yml_path):
    scene_dict = dict()
    all_out_nodes = get_all_out_nodes()
    if not all_out_nodes:
        return
    for node in all_out_nodes:
        node = str(node)
        n = Node(node)
        node_dict = n.parse_node()
        scene_dict[node] = node_dict
    yml_operation.set_yaml_path(yml_path, scene_dict)
