__author__ = 'heshuai'

import pymel.core as pm


def show_material():
    sel_objs = pm.ls(sl=1)
    if sel_objs:
        sel_obj = sel_objs[0]
    try:
        sg_node = sel_obj.getShape().outputs(type='shadingEngine')[0]
        material = pm.listConnections(sg_node.surfaceShader, source=1)[0]
        if material:
            pm.mel.eval('showEditor %s' % material)
            pm.select(material, r=1, ne=1)
        else:
            pm.mel.eval('showEditor %s' % sg_node)
            pm.select(sg_node, r=1, ne=1)
    except:pass
