#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_group_light
# description : ''
# author      : HeShuai
# date        : 2016/1/5
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
# Third-party modules
import maya.cmds as mc
# Studio modules

# Local modules


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_group_light_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


def undo(func):
    def _undo(*args, **kwargs):
        try:
            mc.undoInfo(ock=1)
            result = func(*args, **kwargs)
        except Exception, e:
            raise e
        else:
            return result
        finally:
            mc.undoInfo(cck=1)
    return _undo


def group_selected():
    group_name = None
    selected = mc.ls(sl=1)
    if selected:
        group_name = mc.group(selected)
    return group_name, selected


def add_attr(group_name):
    # add color attr
    mc.addAttr(group_name, longName='color', usedAsColor=True, attributeType='float3')
    mc.addAttr(group_name, longName='redBow', attributeType='float', parent='color')
    mc.addAttr(group_name, longName='greenBow', attributeType='float', parent='color')
    mc.addAttr(group_name, longName='blueBow', attributeType='float', parent='color')
    mc.setAttr('%s.color' % group_name, 1.0, 1.0, 1.0, type='double3')
    # add intensity attr
    mc.addAttr(group_name, longName='intensity', attributeType='double', dv=1, min=0, max=100)
    # add ai_use_color_temperature attr
    mc.addAttr(group_name, longName='Use_Color_Temperature', attributeType='bool', min=0, max=1, dv=0)
    # add ai_color_temperature attr
    mc.addAttr(group_name, longName='Temperature', attributeType='long', min=1500, max=15000, dv=6500)
    # add aiExposure attr
    mc.addAttr(group_name, longName='Exposure', attributeType='double', min=-5, max=1000, dv=0)
    # add aiSamples attr
    mc.addAttr(group_name, longName='Samples', attributeType='long', min=0, max=10, dv=1)
    # add aiRadius attr
    mc.addAttr(group_name, longName='Radius', attributeType='double', min=0, max=10, dv=0)
    # add aiCastShadows attr
    mc.addAttr(group_name, longName='Cast_Shadows', attributeType='bool', min=0, max=1, dv=1)
    # add aiResolution attr
    mc.addAttr(group_name, longName='Area_Light_Resolution', attributeType='long')


def connect_attr(group_name, selected):
    attr_dict = {'color': 'color',
                 'intensity': 'intensity',
                 'Use_Color_Temperature': 'ai_use_color_temperature',
                 'Temperature': 'ai_color_temperature',
                 'Exposure': 'aiExposure',
                 'Samples': 'aiSamples',
                 'Radius': 'aiRadius',
                 'Cast_Shadows': 'aiCastShadows',
                 'Area_Light_Resolution': 'aiResolution'}
    selected_shapes = [mc.ls(sel, dag=1, shapes=1)[0] for sel in selected]
    if not selected_shapes:
        return
    for selected_shape in selected_shapes:
        for attr in attr_dict:
            try:
                mc.connectAttr('%s.%s' % (group_name, attr), '%s.%s' % (selected_shape, attr_dict[attr]))
            except Exception as e:
                print '[AAS] error: %s' % e


@undo
def main():
    group_name, selected = group_selected()
    if selected:
        add_attr(group_name)
        connect_attr(group_name, selected)
    else:
        logging.warning('Nothing selected')


if __name__ == "__main__":
    main()
