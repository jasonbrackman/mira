# -*- coding：utf-8 -*-
# __author__ = "heshuai"
# description="""  """


import pymel.core as pm


def get_meshes_of_sg(sg_node):
    meshes = []
    for i in sg_node.inputs():
        if i.type() == 'transform':
            for j in pm.ls(i, ap=1, dag=1, lf=1):
                if j.type() in ['mesh', 'nurbsSurface']:
                    meshes.append(j)
    meshes = list(set(meshes))
    return meshes