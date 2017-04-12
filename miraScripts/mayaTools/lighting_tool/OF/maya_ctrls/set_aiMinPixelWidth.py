#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """

import pymel.core as pm


def get_selected_objects():
    selected_objects = []
    for i in pm.ls(sl=1):
        if i.type() in ['pgYetiMaya', 'hairSystem', 'shaveHair']:
            selected_objects.append(i)
        else:
            if i.type() == 'transform':
                children = pm.ls(i, ap=1, dag=1, lf=1)
                for child in children:
                    if child.type() in ['pgYetiMaya', 'hairSystem', 'shaveHair']:
                        selected_objects.append(child)
    selected_objects = list(set(selected_objects))
    return selected_objects


def set_aiMinPixelWidth():
    value = raw_input()
    if value:
        if get_selected_objects():
            for i in get_selected_objects():
                try:
                    i.aiMinPixelWidth.set(float(value))
                except:
                    print '[OF] error: %s\'aiMinPixelWidth can\'t be set' % i
        else:
            print '[OF] info: Nothing selected'


if __name__ == '__main__':
    set_aiMinPixelWidth()