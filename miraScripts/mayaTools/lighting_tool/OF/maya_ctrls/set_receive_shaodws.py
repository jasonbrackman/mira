# coding=utf-8
# __author__ = "heshuai"
# description="""  """

import pymel.core as pm
import get_selected_objects


def set_receive_shadows(value):
    selected_objects = get_selected_objects.get_selected_objects()
    if selected_objects:
        for obj in selected_objects:
            try:
                obj.receiveShadows.set(value)
            except:pass