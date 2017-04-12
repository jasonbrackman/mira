# -*- coding: utf-8 -*-
import maya.cmds as mc


def sort_shape(shape_list):
    if len(shape_list) != 2:
        print "[MIRA Warning] shape must contain normal shape and deformed shape"
        return
    if not shape_list[1].endswith("Deformed"):
        shape_list.reverse()
    if not shape_list[1].endswith("Deformed"):
        return
    return shape_list


def assign_shader_to_another(shape_list):
    if not shape_list:
        return
    shape = shape_list[0]
    deformed = shape_list[1]
    shape_sg_connection_attrs = mc.listConnections(shape, c=1, s=0, d=1, p=1, type="shadingEngine")
    if not shape_sg_connection_attrs:
        print "[MIRA Warning] %s has no shadingEngine connection." % shape
        return
    if len(shape_sg_connection_attrs) != 2:
        print "[MIRA Warning] %s shadingEngine connection wrong." % shape
        return
    deformed_sg_connection_attrs = mc.listConnections(deformed, c=1, s=0, d=1, p=1, type="shadingEngine")
    if deformed_sg_connection_attrs:
        if len(deformed_sg_connection_attrs) == 2:
            mc.disconnectAttr(*deformed_sg_connection_attrs)
    try:
        mc.disconnectAttr(*shape_sg_connection_attrs)
        deformed_attr = shape_sg_connection_attrs[0].replace(shape, deformed)
        mc.connectAttr(deformed_attr, shape_sg_connection_attrs[1], f=1)
        print "[MIRA Info] connectAttr %s ---> %s" % (deformed_attr, shape_sg_connection_attrs[1])
    except Exception as e:
        print "[MIRA warning] %s" % e


def lgt_assign_shader_deformed(ref_node):
    if not mc.objExists(ref_node):
        print "[MIRA Info] %s not exist." % ref_node
        return
    outliner_group = mc.referenceQuery(ref_node, dagPath=1, nodes=1)[0]
    meshes = mc.listRelatives(outliner_group, ad=1, ni=1, type="mesh")
    transforms = [mc.listRelatives(mesh, parent=1)[0] for mesh in meshes]
    transforms = list(set(transforms))
    for transform in transforms:
        shapes = mc.listRelatives(transform, s=1)
        shape_list = sort_shape(shapes)
        assign_shader_to_another(shape_list)
