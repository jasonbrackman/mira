__author__ = 'heshuai'

import pymel.core as pm


def get_selected_objects():
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