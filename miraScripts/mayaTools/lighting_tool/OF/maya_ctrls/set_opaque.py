__author__ = 'heshuai'


import pymel.core as pm
import get_selected_objects


def set_opaque(value):
    sel_objects = get_selected_objects.get_selected_objects()
    if sel_objects:
        for obj in sel_objects:
            try:
                obj.aiOpaque.set(value)
            except:pass