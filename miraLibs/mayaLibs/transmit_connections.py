# -*- coding: utf-8 -*-
import pymel.core as pm


def convert_to_PyNode(node):
    if isinstance(node, basestring) and pm.objExists(node):
        return pm.PyNode(node)


def transmit_connections(source_node, target_node, delete_source=True):
    source_node = convert_to_PyNode(source_node)
    target_node = convert_to_PyNode(target_node)
    if not all((source_node, target_node)):
        print "node is not exist."
        return
    source_attrs = source_node.inputs(p=1)
    for source_attr in source_attrs:
        des_attrs = source_attr.outputs(p=1)
        for des_attr in des_attrs:
            if des_attr.node() == source_node:
                new_des_attr = pm.PyNode(des_attr.name().replace(source_node.name(), target_node.name()))
                source_attr // des_attr
                source_attr >> new_des_attr
    tar_attrs = source_node.outputs(p=1)
    for tar_attr in tar_attrs:
        source_attrs = tar_attr.inputs(p=1)
        for source_attr in source_attrs:
            if source_attr.node() == source_node:
                new_source_attr = pm.PyNode(source_attr.name().replace(source_node.name(), target_node.name()))
                source_attr // tar_attr
                try:
                    new_source_attr >> tar_attr
                except:pass
    if delete_source:
        pm.delete(source_node)
