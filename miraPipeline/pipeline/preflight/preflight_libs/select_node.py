# -*- coding: utf-8 -*-
import get_engine


def select_in_maya(nodes):
    import maya.cmds as mc
    if isinstance(nodes, basestring):
        if mc.objExists(nodes):
            mc.select(nodes, r=1)
        else:
            print "%s is not exist" % nodes
    elif isinstance(nodes, list):
        mc.select(nodes, r=1)


def select_in_nuke(nodes):
    import nuke
    import nukescripts
    nukescripts.clear_selection_recursive()
    if isinstance(nodes, basestring):
        nodes = [nodes]
    for node in nodes:
        n = nuke.toNode(node)
        n.knob('selected').setValue(True)


def select_node(nodes):
    engine = get_engine.get_engine()
    if engine == "maya":
        select_in_maya(nodes)
    elif engine == "nuke":
        select_in_nuke(nodes)
    else:
        # todo add other engine method
        return
