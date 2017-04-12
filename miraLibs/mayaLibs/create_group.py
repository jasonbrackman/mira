# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc


def create_group(name, parent=None, lock=False):
    logger = logging.getLogger(__name__)
    if not mc.objExists(name):
        mc.select(clear=1)
        mc.group(name=name, empty=1)
        if lock:
            mc.lockNode(name, l=1)
    if parent:
        if not mc.objExists(parent):
            logger.warning("%s is not exist." % parent)
            return
        current_parent = mc.listRelatives(name, parent=1)
        if current_parent and current_parent[0] == parent:
            logger.info("%s is already a child of %s" % (name, parent))
            return
        mc.parent(name, parent)
