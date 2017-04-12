__author__ = 'heshuai'


import pymel.core as pm
import get_selected_objects


def set_diffuse_visible(value):
    sel_objects = get_selected_objects.get_selected_objects()
    for obj in sel_objects:
        try:
            obj.aiVisibleInDiffuse.set(value)
        except:pass