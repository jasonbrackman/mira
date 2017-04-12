# -*- coding: utf-8 -*-
import maya.cmds as cmds


def remove(name):
    all_namespace = cmds.namespaceInfo(listOnlyNamespaces=1)
    if name not in all_namespace:
        print "%s is not a namespace" % name
        return
    children = cmds.namespaceInfo(name, lon=1)
    if children:
        for child in children:
            remove(child)
    try:
        cmds.namespace(mv=(name, ':'), f = 1)
        cmds.namespace(rm=name)
    except:
        print "## Failed:", name
    else:
        print "// Removed:", name


def remove_namespace():
    cmds.namespace(set=':')
    for name in cmds.namespaceInfo(lon=1):
        if name not in ('UI', 'shared'):
            remove(name)
    print '// Namespaces Clean-Up Completed'


if __name__ == '__main__':
    remove_namespace()
