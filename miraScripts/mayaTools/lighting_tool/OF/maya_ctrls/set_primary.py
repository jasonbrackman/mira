__author__ = 'heshuai'


import pymel.core as pm
import get_selected_objects


def set_primary(value):
    sel_objects = get_selected_objects.get_selected_objects()
    if sel_objects:
        for obj in sel_objects:
            try:
                obj.primaryVisibility.set(value)
            except:pass