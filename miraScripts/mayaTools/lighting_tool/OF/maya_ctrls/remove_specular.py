#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """

import pymel.core as pm
import maya.cmds as mc
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


def undo(func):
    def _undo(*args, **kwargs):
        try:
            mc.undoInfo(ock=1)
            result = func(*args, **kwargs)
        except Exception, e:
            raise e
        else:
            return result
        finally:
            mc.undoInfo(cck=1)
    return _undo


def get_object_list():
    selected_objects = []
    for i in pm.ls(sl=1):
        if i.type() in ['mesh', 'nurbsSurface']:
            selected_objects.append(i)
        else:
            if i.type() == 'transform':
                children = pm.ls(i, ap=1, dag=1, lf=1)
                for child in children:
                    if child.type() in ['mesh', 'nurbsSurface']:
                        selected_objects.append(child)
    selected_objects = list(set(selected_objects))
    return selected_objects


def get_sg_node(mesh):
    sg_nodes = mesh.outputs(type='shadingEngine')
    if sg_nodes:
        return sg_nodes
    else:
        return


def get_material(sg_node):
    material = pm.listConnections(sg_node.surfaceShader, s=1, d=0, p=0)
    if material:
        return material
    else:
        return


@undo
def main():
    sg_nodes = list()
    material = list()
    meshes = get_object_list()
    if meshes:
        for mesh in meshes:
            temp_sg = get_sg_node(mesh)
            if temp_sg:
                sg_nodes.extend(temp_sg)
        sg_nodes = list(set(sg_nodes))
        if sg_nodes:
            for sg_node in sg_nodes:
                temp_material = get_material(sg_node)
                material.extend(temp_material)
        material = list(set(material))
        if material:
            for mat in material:
                if mat.type() == 'aiStandard':
                    try:
                        mat.Ks.set(0)
                    except Exception, e:
                        print e
                elif mat.type() == 'blinn':
                    try:
                        mat.specularRollOff.set(0)
                    except Exception, e:
                        print e
    else:
        msg_box = QMessageBox.information(None, 'Information', 'Nothing Selected')


if __name__ == '__main__':
    main()