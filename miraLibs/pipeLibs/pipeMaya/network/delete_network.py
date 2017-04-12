# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc


def delete_network():
    logger = logging.getLogger(__name__)
    if not mc.objExists("ROOT"):
        logger.error("ROOT node does not exist")
        return
    mc.lockNode("ROOT", lock=False)
    mc.delete("ROOT")

