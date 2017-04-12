__author__ = 'heshuai'


import pymel.core as pm
import get_selected_objects


def set_subdivision(*args):
    sel_objects = get_selected_objects.get_selected_objects()
    if sel_objects:
        for obj in sel_objects:
            obj.aiSubdivType.set(args[0])
            obj.aiSubdivIterations.set(args[1])