__author__ = 'heshuai'


import maya.cmds as mc


def assign_material(meshes, sg_node):
    if meshes and mc.objExists(sg_node):
        mc.sets(meshes, fe=sg_node)