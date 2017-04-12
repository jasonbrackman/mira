# coding=utf-8
# __author__ = "heshuai"
# description="""  """

import pymel.core as pm
import get_selected_objects


def set_displacement_height(value):
    sel_objects = get_selected_objects.get_selected_objects()
    if sel_objects:
        for obj in sel_objects:
            try:
                obj.aiDispHeight.set(value)
            except:pass